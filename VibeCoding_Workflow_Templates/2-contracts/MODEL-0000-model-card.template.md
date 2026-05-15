---
id: MODEL-NNNN
title: "ML Model Card Template"
status: draft        # draft | active | deprecated | superseded | archived
tier: 2-contracts
owner: HYBRID (AI-drafts, human-approves)
last-reviewed: <YYYY-MM-DD>
last-synced-with: <git-commit-sha>
sync-source: code | doc       # code-first → code; contract-first → doc
source-paths:
  - src/models/<model-name>/
  - ml/experiments/<experiment-id>/
synced-at: <YYYY-MM-DD>
product-version: null
supersedes: null
superseded-by: null
---


> **⚠️ WORKED EXAMPLE — DELETE BEFORE USE**
> Concrete names below (revenue-forecast, LightGBM, BigQuery ML, etc.) come
> from a worked e-commerce ML example to give AI strong few-shot context. **Replace
> them with your domain's terms** when filling for your project. The structure (sections,
> tables, frontmatter) is what to keep; the example content is what to swap or delete.
> If your domain doesn't fit (CLI / library / ML / embedded), the example is still
> useful as a structural reference — copy the shape, change the words.

# ML 模型卡 — `<模型名稱>`

> **Tier**: 2-contracts — ML model specification and behavioral contract; must stay synced with model registry
>
> **Why a dedicated doc**: ML models are code + data + configuration, none of which is easily readable as a diff. Without a model card, consumers don't know what the model was trained on, what it's allowed to do, or when to distrust its outputs. This template encodes model intent as a first-class contract — linked to the traceability matrix and subject to change governance.
>
> **Inspired by**: [Google Model Cards](https://modelcards.withgoogle.com/about); adapted for engineering teams.
>
> **Companion fields**: this model's row in `2-contracts/TM-0000-traceability-matrix.template.md` §ML Model Coverage points back here.

---

## 1. 模型總覽

| 欄位 | 值 |
|---|---|
| 模型名稱 | `<e.g. revenue-forecast-v2>` |
| 模型 ID | `MODEL-NNNN` |
| 版本 | `v2.1.0` |
| 模型類型 | 監督式 / 非監督式 / 強化學習 / 基礎模型微調 |
| 任務類型 | 回歸 / 二元分類 / 多類別分類 / 排序 / 生成 |
| 框架 | `<e.g. LightGBM 4.1.0 / PyTorch 2.2.0 / scikit-learn 1.4.0>` |
| 模型格式 | `<e.g. ONNX / pickle / SavedModel / GGUF>` |
| 負責團隊 | `<ml-team>` |
| 模型 Owner | `<name>` |
| 相依 Flow ID | `BF-NNNN`, `SF-NNNN` |
| 實驗 ID | `<MLflow run ID / W&B run ID>` |

---

## 2. 預期用途（Intended Use）

### 2.1 主要用途

- **用途描述**：預測未來 7 天每日訂單收入，用於庫存規劃與行銷預算分配。
- **目標使用者**：供應鏈分析師、行銷經理（透過 BI Dashboard 間接使用）；後端 API 消費（透過 `forecast-service`）。
- **決策自主性**：模型輸出**僅作為參考**；超過 $50,000 的決策需人工審核。

### 2.2 超出範圍的用途（Out-of-Scope）

| 不應使用於 | 原因 |
|---|---|
| 個別使用者行為預測 | 訓練資料為聚合層級，個體預測無意義 |
| 超過 30 天的長期預測 | 訓練時間範圍限制；誤差隨時間快速累積 |
| 新市場 / 新品類（上線 < 6 個月） | 訓練資料不足；模型無法泛化 |
| 用於員工績效評估 | 倫理風險；非設計用途 |

---

## 3. 訓練資料

### 3.1 資料來源

| 資料集 | 版本 / 快照日期 | 管線 |
|---|---|---|
| `analytics.daily_revenue` | `2022-01-01 ~ 2024-06-30` | `PIPE-NNNN` |
| `marketing.campaign_spend` | `2022-01-01 ~ 2024-06-30` | `PIPE-NNNN` |
| `external.holiday_calendar` | 版本 `2024-Q2` | 手動上傳 |

### 3.2 資料集規模與切分

| 切分 | 時間範圍 | 樣本數 |
|---|---|---|
| 訓練集 | 2022-01-01 ~ 2024-03-31 | ~850 筆（每日聚合） |
| 驗證集 | 2024-04-01 ~ 2024-05-31 | ~60 筆 |
| 測試集 | 2024-06-01 ~ 2024-06-30 | ~30 筆（holdout，訓練後才使用一次） |

> **切分策略**：時序資料採時間順序切分（不隨機切分，以防未來洩漏）。

### 3.3 預處理步驟

1. 移除 `revenue_usd = 0` 的假日 / 關店日
2. 對數轉換（`log1p`）目標變數以降低偏態
3. 滾動統計特徵（7天/30天移動平均、滾動標準差）
4. 節假日 one-hot 編碼
5. 缺失值填補：`campaign_spend` 缺失值以 0 填補

### 3.4 已知資料偏差（Known Biases）

| 偏差來源 | 描述 | 緩解措施 |
|---|---|---|
| 新冠疫情期（2020-2021） | 銷售模式異常，已排除在訓練集外 | 訓練集起始於 2022-01-01 |
| 季節性 | 訓練集未完整涵蓋 3 個完整年度 | 已加入季節性特徵；持續監控 |
| 促銷活動 | 大型促銷期間的異常高收入可能過擬合 | 加入促銷標記特徵 |

---

## 4. 評估

### 4.1 指標定義

| 指標 | 定義 | 說明 |
|---|---|---|
| MAPE | 平均絕對百分比誤差 | 主要業務指標 |
| RMSE | 均方根誤差（USD） | 工程監控指標 |
| P90 誤差 | 90th percentile 絕對誤差 | 極端值容忍度 |
| 方向準確率 | 預測趨勢與實際趨勢一致的比例 | 業務決策輔助指標 |

### 4.2 測試集效能

| 指標 | 測試集結果 | 基準線（naïve 7-day lag） | 是否達標 |
|---|---|---|---|
| MAPE | 8.2% | 15.4% | 是 (目標 < 12%) |
| RMSE | $2,340 | $4,100 | 是 |
| P90 誤差 | $4,800 | $8,200 | 是 |
| 方向準確率 | 74% | 58% | 是 (目標 > 70%) |

### 4.3 公平性分析

| 切片 | MAPE | 備注 |
|---|---|---|
| 週一至週五 | 7.1% | 工作日預測較穩定 |
| 週末 | 11.4% | 週末方差較大 |
| 節假日前後 | 18.3% | 已知弱點；節假日建議人工審核 |
| 新品類（< 6 個月） | 35%+ | **超出範圍**；不應信任 |

### 4.4 已知失效模式

| 情境 | 模型行為 | 建議處理 |
|---|---|---|
| 突發促銷（未在訓練集中） | 嚴重低估（-40% ~ -60%） | 促銷期前人工調整係數 |
| 連假首日 / 末日 | 系統性低估 | 節假日校正模組（規劃中） |
| 原始資料延遲 > 2 小時 | 使用陳舊特徵；預測品質下降 | 資料延遲時凍結預測並告警 |

---

## 5. 部署

### 5.1 服務基礎設施

| 欄位 | 值 |
|---|---|
| 服務名稱 | `forecast-service` |
| 部署平台 | Kubernetes (GKE) |
| 推論框架 | `<e.g. BentoML / Seldon / custom FastAPI>` |
| 模型儲存 | `<e.g. GCS: gs://ml-models/revenue-forecast/v2/>` |
| 模型載入方式 | 啟動時載入（in-process inference） |

### 5.2 效能目標

| 指標 | 目標 | 量測方式 |
|---|---|---|
| 推論延遲 P99 | < 200ms | Prometheus histogram |
| 吞吐量 | ≥ 100 RPS | 壓力測試 |
| 模型大小 | < 50MB | CI artifact check |
| 記憶體使用 | < 512MB per pod | K8s resource limit |

### 5.3 A/B 測試計畫

| 欄位 | 值 |
|---|---|
| 實驗框架 | `<e.g. LaunchDarkly / 自建 feature flag>` |
| Control | `revenue-forecast-v1`（現行模型） |
| Treatment | `revenue-forecast-v2`（此模型） |
| 流量切分 | Control 80% / Treatment 20% |
| 成功指標 | Treatment MAPE 比 Control 低 ≥ 2 個百分點，持續 14 天 |
| 失敗回滾條件 | Treatment MAPE > Control MAPE + 3%，持續 3 天 |

---

## 6. 倫理考量（Ethical Considerations）

### 6.1 潛在危害

| 危害類型 | 描述 | 可能性 | 嚴重度 |
|---|---|---|---|
| 錯誤預測導致庫存積壓 | 過度樂觀預測 → 過量採購 | 中 | 中 |
| 錯誤預測導致庫存短缺 | 過度悲觀預測 → 銷售機會損失 | 中 | 中 |
| 對新市場的系統性低估 | 新市場資料不足；偏見持續 | 高 | 低（已文件化） |

### 6.2 緩解措施

- 所有預測值附帶 **90% 預測區間**，強迫消費者理解不確定性
- 超過 $50,000 決策強制要求人工審核（系統層面阻擋）
- 新品類自動標記警告，拒絕提供預測值
- 每季進行公平性審查，識別系統性偏差

### 6.3 人工介入要求（Human-in-the-Loop）

| 決策情境 | 人工介入要求 |
|---|---|
| 預測值 > $500,000 / 天 | 必須人工審核 |
| 節假日期間預測 | 建議人工校正 |
| 新品類 / 新市場 | 禁止使用模型預測 |
| 模型漂移告警觸發 | 暫停自動決策；等待人工確認 |

---

## 7. 維護

### 7.1 重訓節奏

| 觸發條件 | 行動 |
|---|---|
| 排程：每月 1 日 | 使用最新 90 天資料增量訓練 |
| 漂移觸發：PSI > 0.2 | 立即啟動緊急重訓 |
| 業務觸發：新品類上線 | 評估是否需要重訓或分群建模 |

### 7.2 漂移監控

| 監控類型 | 指標 | 告警閾值 | 告警通知 |
|---|---|---|---|
| 資料漂移（輸入分佈）| PSI（Population Stability Index） | > 0.2 | PagerDuty |
| 概念漂移（預測品質）| 過去 7 天 MAPE vs 基準 | > 基準 + 5% | Slack #ml-alerts |
| 特徵重要性漂移 | Top-3 特徵排名變動 | 排名變動 ≥ 2 位 | Slack #ml-alerts |

### 7.3 告警閾值

| 告警 | 條件 | 嚴重度 |
|---|---|---|
| 模型服務宕機 | 推論端點回應 5xx | Critical — PagerDuty |
| 推論延遲過高 | P99 > 500ms 持續 5 分鐘 | Warning — Slack |
| 資料漂移 | PSI > 0.2 | Critical — PagerDuty |
| 預測品質下降 | 7日 MAPE > 15% | Warning — Slack |

---

## 8. 模型血緣（Lineage）

| 欄位 | 值 |
|---|---|
| 實驗 ID | `<MLflow: exp-0042 / W&B: run-abc123>` |
| 父模型 | `revenue-forecast-v1` (`MODEL-NNNN-1`) |
| 訓練程式碼 git commit | `<commit-sha>` |
| 訓練資料集版本 | `analytics.daily_revenue@snapshot:2024-07-01` |
| Feature Store 版本 | `<feature-group>@v3` |
| 超參數 | 見實驗 ID 連結 |
| 訓練日期 | `<YYYY-MM-DD>` |
| 訓練環境 | `<e.g. GCP Vertex AI / local GPU / CI>` |

---

## See also

- `2-contracts/PIPE-0000-pipeline-contract.template.md` — 訓練資料管線契約
- `2-contracts/API-0000-api-spec.template.md` — 推論 API 端點規格
- `2-contracts/SLO-0000-slo-spec.template.md` — 模型服務 SLO
- `2-contracts/TM-0000-traceability-matrix.template.md` — §ML Model Coverage
- `3-process/PROC-0009-incident-response.template.md` — 模型失效的事故回應
- `4-exploration/CIA-0000-change-impact-analysis.template.md` — 模型架構 / 訓練資料變更需 CIA
- `.claude/rules/change-governance.md` — ML model 變更觸發 "external integration" / "architecture boundary" CIA gate
