---
id: EXP-NNNN
title: "ML 實驗記錄"
status: draft
tier: 4-exploration
owner: HYBRID (AI-drafts, human-approves)
last-reviewed: <YYYY-MM-DD>
product-version: null
supersedes: null
superseded-by: null
---

> **⚠️ WORKED EXAMPLE — DELETE BEFORE USE**
> Concrete names below (ChurnPredictor, customer_events, XGBoost, AUROC, etc.) come
> from a worked churn-prediction ML example to give AI strong few-shot context. **Replace
> them with your domain's terms** when filling for your project. The structure (sections,
> tables, frontmatter) is what to keep; the example content is what to swap or delete.
> If your domain doesn't fit (CV / NLP / time-series / RL), the example is still
> useful as a structural reference — copy the shape, change the words.

# EXP-NNNN: <實驗簡稱>

> **Tier**: 4-exploration — ML/data-science experiment log (per-experiment ephemeral; archive after decision)
> **Status**: running | completed | abandoned

---

## 1. 實驗概要

| 項目 | 內容 |
|---|---|
| **實驗名稱** | `exp-<NNNN>-<short-slug>` (e.g. `exp-0042-xgb-feature-recency`) |
| **假說** | 加入最近 30 天行為特徵後，AUROC 可提升 ≥ 3 個百分點 |
| **成功指標** | AUROC ≥ 0.82 (baseline: 0.79) |
| **基準值** | baseline AUROC = 0.79，precision@10% = 0.61 |
| **目標提升** | AUROC +0.03；次要：precision@10% +0.05 |
| **最長時限** | 2 週；超時則評估是否放棄 |
| **負責人** | <name> |
| **建立日期** | YYYY-MM-DD |

---

## 2. 實驗設計

| 設計項目 | 說明 |
|---|---|
| **自變數 (Independent Variables)** | 最近 7/14/30 天登入次數、購買金額、頁面停留時間 |
| **控制組 (Control)** | 現有 ChurnPredictor v1.2（不含時間衰減特徵） |
| **實驗組 (Treatment)** | ChurnPredictor v1.3 加入 recency 特徵集 `FST-0007` |
| **樣本量** | 訓練集 120,000 筆；測試集 30,000 筆（80/20 時間切分） |
| **實驗期間** | 2026-05-01 → 2026-05-14（使用靜態快照，非線上 A/B） |
| **統計檢定** | DeLong test (AUROC 差異)；顯著水準 α = 0.05 |
| **避免資料洩露** | 特徵計算以訓練截止日為界，測試集標籤 t+30 天後揭露 |

---

## 3. 資料集

| 項目 | 說明 |
|---|---|
| **訓練集版本** | `customer_events_v3.2_20260401` (DVC tag: `ds/train-v3.2`) |
| **測試集版本** | `customer_events_v3.2_20260501` (DVC tag: `ds/test-v3.2`) |
| **特徵集 ID** | `FST-0007` (登記於 feature store；含 recency 欄位) |
| **標籤定義** | 30 天內無活躍行為 = churned (1)；否則 = retained (0) |
| **類別不平衡** | churned : retained ≈ 1 : 9；訓練採 SMOTE 過採樣 |

### 資料前處理步驟

1. 移除最後 30 天有購買行為的用戶（label leakage 防護）
2. 填補缺失值：數值欄位取中位數；類別欄位取眾數
3. 對數轉換：`purchase_amount_log = log1p(purchase_amount)`
4. 標準化：Z-score，使用訓練集統計量（scaler 序列化後供推論用）
5. 時間切分：依 `event_date` 排序後分割，**禁止隨機 shuffle 後分割**

---

## 4. 模型配置

### 模型類型

`XGBoost 2.0.3` — 選擇理由：與現有 ChurnPredictor v1.2 同框架，便於孤立特徵貢獻。

### 超參數

| 超參數 | 控制組值 | 實驗組值 | 備註 |
|---|---|---|---|
| `n_estimators` | 300 | 300 | 固定，單純比較特徵差異 |
| `max_depth` | 6 | 6 | 固定 |
| `learning_rate` | 0.05 | 0.05 | 固定 |
| `subsample` | 0.8 | 0.8 | 固定 |
| `colsample_bytree` | 0.8 | 0.8 | 固定 |
| `scale_pos_weight` | 9 | 9 | 因應類別不平衡 |
| `random_state` | 42 | 42 | 固定，確保可重現 |

### 框架與硬體

| 項目 | 規格 |
|---|---|
| **框架** | Python 3.11, XGBoost 2.0.3, scikit-learn 1.4, pandas 2.2 |
| **訓練硬體** | GCP `n1-standard-8` (8 vCPU, 30 GB RAM) |
| **預估訓練時間** | ~12 min / run |
| **Notebook 路徑** | `notebooks/exp-0042-xgb-feature-recency.ipynb` |

---

## 5. 結果

### 指標比較

| 指標 | 控制組 (v1.2) | 實驗組 (v1.3) | 差異 | 達標？ |
|---|---|---|---|---|
| AUROC | 0.790 | 0.821 | +0.031 | ✓ |
| precision@10% | 0.610 | 0.648 | +0.038 | △ (差 0.012) |
| F1 (threshold=0.5) | 0.541 | 0.572 | +0.031 | — |
| Log Loss | 0.381 | 0.354 | -0.027 | — |
| 訓練時間 | 11.2 min | 13.8 min | +2.6 min | acceptable |
| 推論延遲 P99 | 4.2 ms | 5.1 ms | +0.9 ms | acceptable |

### 統計顯著性

- DeLong test p-value: **0.0023** (< α=0.05) → AUROC 差異顯著
- 95% 信賴區間 for ΔAUROC: [+0.018, +0.044]
- 結論：實驗組 AUROC 提升在統計上顯著

---

## 6. 分析與洞察

### 有效的部分

- `login_count_7d`（最近 7 天登入次數）貢獻最大，feature importance rank #2（原 rank #8）
- Recency 特徵對高流失風險用戶（score > 0.7）discriminability 顯著提升

### 無效的部分

- `page_dwell_time_30d`（30 天停留時間）增益幾乎為零（importance < 0.001）；建議下次實驗剔除
- precision@10% 未達目標（+0.038 vs 目標 +0.05）；可能需要閾值校準或 cost-sensitive 訓練

### 誤差分析

| 錯誤類型 | 樣本數 | 主要特徵模式 |
|---|---|---|
| False Negative (churned 預測為 retained) | 1,240 | 近期有少量購買但購買金額極低 |
| False Positive (retained 預測為 churned) | 890 | 季節性休眠用戶（每年固定月份不活躍） |

季節性休眠用戶誤判建議後續加入「歷史活躍季節」特徵（`FST-0009` 候選）。

### 特徵重要性 (Top 5)

| Rank | 特徵 | Importance Score |
|---|---|---|
| 1 | `purchase_amount_log` | 0.187 |
| 2 | `login_count_7d` | 0.143 |
| 3 | `days_since_last_purchase` | 0.121 |
| 4 | `login_count_30d` | 0.098 |
| 5 | `support_ticket_count` | 0.076 |

---

## 7. 決策

| 項目 | 內容 |
|---|---|
| **決策** | **Deploy（部署）** |
| **決策日期** | YYYY-MM-DD |
| **理由** | AUROC 主要指標達標且統計顯著；precision 雖未達目標但提升方向正確，接受後續微調 |
| **後續動作** | 1. 上線 v1.3 至 staging 進行影子測試；2. 開立 EXP-0043 針對季節性特徵改善 precision |
| **下一個實驗 ID** | EXP-0043（季節性休眠特徵） |

> 若決策為 **Iterate**：填寫「下一個實驗 ID」並在新實驗單引用本 EXP-NNNN 作為前因。
> 若決策為 **Abandon**：記錄原因並在假說欄補充「已証偽」；歸檔本文件。

---

## 8. 可重現性

| 項目 | 值 |
|---|---|
| **Git Commit** | `abc1234` (branch: `exp/0042-xgb-feature-recency`) |
| **Random Seed** | 42（全程：train/test split、SMOTE、XGBoost） |
| **環境規格** | `requirements-exp.txt` @ commit `abc1234`；或 Docker image `ml-train:0042` |
| **Notebook 路徑** | `notebooks/exp-0042-xgb-feature-recency.ipynb` |
| **資料 DVC 標籤** | `ds/train-v3.2`, `ds/test-v3.2` |
| **模型 Artifact** | `gs://ml-artifacts/exp-0042/model.xgb` |
| **復現指令** | `make train EXP=0042` （詳見 `Makefile` target `train`） |

---

## 附錄：實驗狀態追蹤

```
EXP-0040 (baseline v1.2)  ──→  EXP-0042 (recency features)  ──→  EXP-0043 (seasonality)
     deploy                          deploy                         planned
```
