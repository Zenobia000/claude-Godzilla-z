# 監控規格 (Monitoring / Observability Spec) - [專案名稱]

> **版本:** v1.0 | **更新:** YYYY-MM-DD | **狀態:** 草稿/審核中/已批准
> **Owner:** SRE / DevOps，與後端共同維護
> **原則:** 每條 NFR 都要有對應的量測；每個 alert 都要有對應的 Runbook，否則只是噪音。

---

## 1. SLI / SLO

| SLI | 定義 | SLO 目標 | 量測來源 | 對應 NFR |
| :--- | :--- | :--- | :--- | :--- |
| API 可用率 | [成功請求 / 總請求] | [99.9%]/30d | [LB metrics] | NFR-002 |
| API p95 延遲 | | < [X] ms | | NFR-001 |

---

## 2. Metrics / Logs / Traces

| 訊號 | 內容 | 工具 | 保留 |
| :--- | :--- | :--- | :--- |
| **Metrics** | [RED：rate、error、duration；佇列 lag、DLQ 深度] | [Prometheus] | [N 天] |
| **Logs** | [結構化格式、correlation id 欄位、敏感欄位遮罩] | | |
| **Traces** | [關鍵路徑覆蓋清單] | | |

---

## 3. 告警 (Alerts)

| Alert | 條件 | 嚴重度 | 通知對象 | Runbook |
| :--- | :--- | :--- | :--- | :--- |
| APILatencyHigh | p95 > [X] ms 持續 [5] 分鐘 | page | on-call | [`runbook.md`](./runbook.md)（api-latency-high） |
| DLQNotEmpty | DLQ 深度 > 0 | ticket | 團隊頻道 | |

告警設計原則：page 只留「需要人立刻行動」的條件；其餘降為 ticket，避免 on-call 麻痺。

---

## 4. Dashboard

| Dashboard | 讀者 | 內容 |
| :--- | :--- | :--- |
| [服務總覽] | on-call | [SLO 燃燒率、RED 指標] |
| [業務指標] | PM | [工單量、完成率] |

---

## 5. 追溯

- NFR 來源：`../03_architecture/nfr.md`
- 事件通道監控：`../04_design/event_spec.md` §3
- 告警對應處置：本目錄 Runbook；事故覆盤進 [`incident_postmortem.md`](./incident_postmortem.md)
