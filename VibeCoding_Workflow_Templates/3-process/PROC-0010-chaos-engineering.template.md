---
id: PROC-0010
title: "混沌工程 / Game Day 執行手冊"
status: draft
tier: 3-process
owner: HUMAN-ONLY
last-reviewed: <YYYY-MM-DD>
product-version: null
supersedes: null
superseded-by: null
---

> **⚠️ WORKED EXAMPLE — DELETE BEFORE USE**
> Concrete names below (OrderService, PaymentGateway, Redis, checkout-api, etc.) come
> from a worked e-commerce microservices example to give AI strong few-shot context. **Replace
> them with your domain's terms** when filling for your project. The structure (sections,
> tables, frontmatter) is what to keep; the example content is what to swap or delete.
> If your domain doesn't fit (monolith / batch pipeline / embedded), the example is still
> useful as a structural reference — copy the shape, change the words.

# 混沌工程 / Game Day 執行手冊 — [系統名稱]

> **Tier**: 3-process — chaos engineering and game day runbook
>
> **Purpose**: 在受控條件下主動注入故障，驗證系統在異常狀態下的韌性與復原能力。
>
> **Why a dedicated template**: 混沌實驗若缺乏明確的 Steady State 定義與 Abort Criteria，
> 很容易從「受控實驗」變成「真實事故」。本模板確保每次 Game Day 有完整的安全護欄。

---

## 1. 混沌工程原則

| 原則 | 說明 |
|---|---|
| **定義穩態假說 (Steady State Hypothesis)** | 先量化「系統正常」的可觀測指標，才能判斷實驗是否破壞了穩態 |
| **最小化爆炸半徑 (Minimize Blast Radius)** | 從最小影響範圍開始（單一 pod、單一可用區），逐步擴大範圍 |
| **在真實環境執行 (Run in Production)** | Staging 的行為不等於 Production；最終目標是在 Production 驗證 |
| **自動化實驗** | 手動注入難以重現；工具選型需支援腳本化與 CI 整合 |
| **先有監控，再打混沌** | 沒有可觀測性的混沌實驗等同盲目破壞 |

### 穩態假說定義

在本次 Game Day 開始前，以下指標必須全部處於正常範圍才可繼續：

| 指標 | 正常範圍 | 量測來源 |
|---|---|---|
| checkout API P99 延遲 | < 800 ms | Grafana: `checkout_latency_p99` |
| 訂單成功率 | > 99.5% | Grafana: `order_success_rate` |
| 錯誤率 (5xx) | < 0.1% | Datadog: `error_rate` |
| Redis 命中率 | > 85% | Redis INFO: `keyspace_hits / (hits + misses)` |
| 支付服務可用性 | 100% | UptimeRobot |

---

## 2. Game Day 計畫

| 項目 | 內容 |
|---|---|
| **日期與時間** | YYYY-MM-DD HH:MM – HH:MM (UTC+8)；選低峰時段 |
| **參與者** | SRE Lead: / Backend Lead: / On-call Engineer: / Observability: |
| **範圍** | Staging 環境；Production 僅在 §3 標記 `prod-safe: yes` 的實驗 |
| **溝通計畫** | Game Day 開始前 30 min 發送 Slack 通知至 `#engineering`；結束後摘要回報 |
| **Abort Criteria（全局終止條件）** | 任一條件觸發即立即停止所有實驗並進入清理流程：|

**全局 Abort Criteria：**
- 生產環境錯誤率 > 1% 持續 2 分鐘
- 任何實驗導致資料遺失或資料庫損毀
- On-call 收到真實 P0/P1 告警
- 參與者判斷情況失控（人工裁量）

---

## 3. 實驗目錄

| # | 實驗名稱 | 目標元件 | 故障類型 | 預期行為 | 實際行為 | 狀態 |
|---|---|---|---|---|---|---|
| CE-01 | Redis 完全斷線 | Cache Layer | dependency timeout | 退化為直查 DB；延遲升高但不失敗 | — | planned |
| CE-02 | OrderService 單一 Pod 殺死 | OrderService | pod kill | 其餘 Pod 接手；P99 短暫升高後恢復 | — | planned |
| CE-03 | 支付閘道高延遲 | PaymentGateway | latency injection (+3s) | timeout 後觸發 retry；超過重試次數回傳 503 | — | planned |
| CE-04 | 網路分區（OrderService → InventoryService） | InventoryService | network partition | 訂單建立降級：不即時扣庫存，進非同步佇列 | — | planned |
| CE-05 | checkout-api CPU 壓力 | checkout-api | CPU stress (80%) | HPA 觸發橫向擴展；延遲不超過 SLO | — | planned |
| CE-06 | 資料磁碟填滿模擬 | DB Node | disk fill (90%) | 告警觸發；應用拒絕寫入並回傳友善錯誤 | — | planned |

**故障類型說明：**

| 故障類型 | 注入方式 |
|---|---|
| network partition | `iptables -A OUTPUT -d <target-ip> -j DROP` |
| latency injection | `tc qdisc add dev eth0 root netem delay 3000ms` |
| pod kill | `kubectl delete pod <pod-name>` |
| CPU stress | `stress-ng --cpu 4 --timeout 300s` |
| disk fill | `fallocate -l 10G /tmp/fill` |
| dependency timeout | 覆寫 env var 將 timeout 設為 1ms；或 Toxiproxy |

---

## 4. 實驗執行步驟

每個實驗依以下標準程序執行，**不可跳過任何步驟**：

```
┌─────────────────────────────────────────────────────────┐
│  每個實驗的標準執行程序                                    │
│                                                         │
│  1. Pre-checks                                          │
│     ├── 確認穩態指標全部正常                               │
│     ├── 確認監控儀表板已開啟                               │
│     └── 所有參與者就位                                    │
│                                                         │
│  2. 注入故障 (Inject Fault)                              │
│     ├── 執行注入指令（見各實驗）                            │
│     └── 記錄注入時間戳 T₀                                 │
│                                                         │
│  3. 觀察 (Observe)                                      │
│     ├── 監控穩態指標變化                                   │
│     ├── 記錄系統反應（告警觸發？自動恢復？）                  │
│     └── 如達 Abort Criteria → 立即執行 Cleanup            │
│                                                         │
│  4. 驗證復原 (Verify Recovery)                           │
│     ├── 移除故障注入                                      │
│     ├── 等待系統回到穩態（≤ RTO 目標）                      │
│     └── 記錄復原時間戳 T₁；MTTR = T₁ - T₀                 │
│                                                         │
│  5. 清理 (Cleanup)                                      │
│     ├── 移除所有臨時 iptables / tc / stress 規則           │
│     ├── 確認所有 Pod 恢復正常副本數                         │
│     └── 記錄本實驗結果至 §6                               │
└─────────────────────────────────────────────────────────┘
```

### CE-01 詳細步驟（以 Redis 斷線為例）

```bash
# Pre-check
kubectl get pods -n production | grep redis
redis-cli -h $REDIS_HOST ping  # 應回傳 PONG

# 注入：封鎖 Redis 連線
kubectl exec -it $APP_POD -- iptables -A OUTPUT -p tcp --dport 6379 -j DROP

# 觀察 3 分鐘：監控 Grafana checkout_latency_p99 與 order_success_rate

# 清理
kubectl exec -it $APP_POD -- iptables -D OUTPUT -p tcp --dport 6379 -j DROP

# 驗證：redis-cli ping 恢復；指標回穩
```

---

## 5. 工具配置

根據團隊環境選擇一種工具；**選定後填入此表，其餘刪除**：

| 工具 | 適用場景 | 設定位置 |
|---|---|---|
| **Chaos Monkey** (Netflix OSS) | AWS/Spinnaker 環境；隨機終止 instance | `chaos-monkey-config.yml` |
| **Litmus** (CNCF) | Kubernetes 原生；ChaosExperiment CRD | `k8s/chaos/litmus/` |
| **Gremlin** (SaaS) | 多雲；無需自建基礎設施；需付費授權 | Gremlin Dashboard |
| **手動（tc / iptables）** | 輕量需求；完全可控；適合初期 | 本 Runbook §4 指令 |
| **Toxiproxy** | 網路層代理注入；適合 HTTP/TCP 服務 | `toxiproxy.json` |

**本系統選擇**: `<填入選擇>`

---

## 6. 結果與發現

### CE-01：Redis 完全斷線

| 項目 | 內容 |
|---|---|
| **結果** | passed / **failed** |
| **注入時間** | YYYY-MM-DD HH:MM |
| **復原時間** | YYYY-MM-DD HH:MM（MTTR: X min） |
| **RTO 目標** | 5 min |
| **RTO 達標** | yes / no |
| **告警觸發** | `redis_connection_failed` @ T₀+45s ✓ |
| **意外行為** | 發現部分請求在 Redis 斷線期間未走 DB fallback，直接回傳 500（預期應降級） |
| **行動項目** | 修正 `CacheService.get()` 的 fallback 邏輯（見 §7-FIX-01） |

> 複製以上區塊為每個實驗填寫一份結果。

---

## 7. 改善計畫

| ID | 發現來源 | 問題描述 | 優先級 | 負責人 | 完成期限 | 驗證方式 |
|---|---|---|---|---|---|---|
| FIX-01 | CE-01 | Redis 斷線時部分請求未走 DB fallback | HIGH | Backend Lead | YYYY-MM-DD | 重跑 CE-01 確認 fallback 生效 |
| FIX-02 | CE-03 | 支付閘道 timeout 未觸發 DLQ，導致訂單懸空 | CRITICAL | SRE | YYYY-MM-DD | 重跑 CE-03 + 驗證 DLQ 有訊息 |
| FIX-03 | CE-05 | HPA 擴展延遲 4 min，超出 SLO | MEDIUM | SRE | YYYY-MM-DD | 調整 HPA `scaleUp.stabilizationWindowSeconds` 後重測 |

---

## 8. 定期排程

| 頻率 | 範圍 | 目標 |
|---|---|---|
| **每月** | Staging 環境；單一服務故障 | 驗證新部署未引入韌性退化 |
| **每季** | Staging + 部分 Production（低峰）；多服務協同故障 | 驗證跨服務依賴的降級策略 |
| **每年** | 完整 Production Game Day | 全面韌性審計；包含 DR 切換演練 |

### 範圍升級計畫

```
Phase 1（現在）: 單一服務 × Staging
     ↓ 穩態假說驗證通過 × 3 個月
Phase 2: 多服務協同 × Staging + Production 低峰
     ↓ 告警覆蓋率 > 95% + MTTR < SLO × 2 個季度
Phase 3: 完整 Production Game Day（含 DR 演練）
```

**升級前提**：前一個 Phase 的所有 CRITICAL/HIGH 改善項目全部完成且驗證通過。
