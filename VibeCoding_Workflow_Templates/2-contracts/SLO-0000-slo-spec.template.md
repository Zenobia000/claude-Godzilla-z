---
id: SLO-NNNN
title: "SLO Specification Template"
status: draft        # draft | active | deprecated | superseded | archived
tier: 2-contracts
owner: HYBRID (AI-drafts, human-approves)
last-reviewed: <YYYY-MM-DD>
last-synced-with: <git-commit-sha>
sync-source: code | doc       # code-first → code; contract-first → doc
source-paths:
  - src/<service>/metrics/
  - infra/alerts/<service>.yaml
synced-at: <YYYY-MM-DD>
product-version: null
supersedes: null
superseded-by: null
---


> **⚠️ WORKED EXAMPLE — DELETE BEFORE USE**
> Concrete names below (OrderService, payment-api, etc.) come
> from a worked e-commerce example to give AI strong few-shot context. **Replace
> them with your domain's terms** when filling for your project. The structure (sections,
> tables, frontmatter) is what to keep; the example content is what to swap or delete.
> If your domain doesn't fit (CLI / library / ML / embedded), the example is still
> useful as a structural reference — copy the shape, change the words.

# SLO 規格 — `<服務名稱>`

> **Tier**: 2-contracts — SRE Service Level Objective specification; must stay synced with monitoring configuration
>
> **Why a dedicated doc**: SLOs are contracts between the service team and its consumers. Without an explicit spec, alert thresholds scatter across monitoring configs, burn-rate decisions become tribal knowledge, and error budget policy never gets enforced. This template makes SLOs a first-class contract artifact — reviewable, diffable, and linked to the traceability matrix.
>
> **Companion fields**: this service's row in `2-contracts/TM-0000-traceability-matrix.template.md` §Non-Functional Coverage points back here.

---

## 1. 服務總覽

| 欄位 | 值 |
|---|---|
| 服務名稱 | `<e.g. order-service>` |
| 服務層級 | Tier 1 (critical) / Tier 2 (important) / Tier 3 (best-effort) |
| 負責團隊 | `<team-name>` |
| On-call 輪值 | `<PagerDuty rotation name>` |
| 版本 | `v<N>` |
| 相依服務（上游） | `payment-service`, `inventory-service` |
| 相依服務（下游消費者） | `notification-service`, `analytics-pipeline` |
| 核心 Flow ID | `BF-NNNN`, `SF-NNNN` |

---

## 2. SLI 定義

> SLI（Service Level Indicator）是可測量的服務品質指標。每個 SLI 必須說明如何測量、從哪裡讀取、以及哪些事件算「有效事件」。

### 2.1 可用性（Availability）

| 欄位 | 值 |
|---|---|
| 定義 | 成功回應數 / 有效請求總數 |
| 測量方式 | HTTP 2xx + 3xx 回應計為成功；4xx（除 429）計為成功；5xx 與 timeout 計為失敗 |
| 資料來源 | Prometheus metric: `http_requests_total{service="order-service"}` |
| 有效事件過濾 | 排除 `/health` 與 `/metrics` 端點；排除合法 401/403 |
| 聚合視窗 | 1 分鐘滾動 |

### 2.2 延遲（Latency）

| 欄位 | 值 |
|---|---|
| 定義 | 請求從收到到回應完成的時間 |
| 測量方式 | Histogram bucket；以 P99 為主要 SLI，P50 為輔助 |
| 資料來源 | Prometheus metric: `http_request_duration_seconds` |
| 有效事件過濾 | 與可用性 SLI 相同排除規則 |
| 聚合視窗 | 5 分鐘滾動 |

### 2.3 吞吐量（Throughput）

| 欄位 | 值 |
|---|---|
| 定義 | 單位時間內成功處理的請求數 |
| 測量方式 | RPS（Requests Per Second） |
| 資料來源 | Prometheus metric: `http_requests_total` rate |
| 有效事件過濾 | 同上 |
| 聚合視窗 | 1 分鐘滾動 |

### 2.4 錯誤率（Error Rate）

| 欄位 | 值 |
|---|---|
| 定義 | 5xx 錯誤數 / 有效請求總數 |
| 測量方式 | HTTP 5xx + timeout |
| 資料來源 | Prometheus metric: `http_requests_total{status=~"5.."}` |
| 有效事件過濾 | 同上 |
| 聚合視窗 | 1 分鐘滾動 |

---

## 3. SLO 目標

### 3.1 目標值

| SLI | 目標（30 天滾動） | 基準線（過去 90 天實測） |
|---|---|---|
| 可用性 | 99.9% | <填入實測值> |
| 延遲 P99 | < 500ms | <填入實測值> |
| 延遲 P50 | < 100ms | <填入實測值> |
| 錯誤率 | < 0.1% | <填入實測值> |

> **設定原則**: SLO 應比過去 90 天實測值低 10-20%，留有改善空間，但不能低於消費者 SLA 要求。

### 3.2 錯誤預算

| 視窗 | SLO 99.9% 對應錯誤預算 |
|---|---|
| 30 天 | 43.8 分鐘 downtime |
| 7 天 | 10.1 分鐘 downtime |
| 1 天 | 1.44 分鐘 downtime |

### 3.3 多視窗多燃燒率告警（Multi-window Multi-burn-rate Alerts）

採用 Google SRE Workbook 建議的 MWMB 策略：

| 告警名稱 | 燃燒率 | 短視窗 | 長視窗 | 嚴重度 | 通知方式 |
|---|---|---|---|---|---|
| Page — 快速燃燒 | 14.4× | 1h | 5min | Critical | PagerDuty (immediate) |
| Page — 慢速燃燒 | 6× | 6h | 30min | Critical | PagerDuty (immediate) |
| Ticket — 中速燃燒 | 3× | 3d | 6h | Warning | Slack #oncall |
| Info — 低速燃燒 | 1× | 3d | — | Info | Slack #sre-digest |

```yaml
# 範例: 快速燃燒 Prometheus rule
- alert: OrderServiceFastBurn
  expr: |
    (
      rate(http_requests_total{service="order-service",status=~"5.."}[5m])
      / rate(http_requests_total{service="order-service"}[5m])
    ) > (14.4 * 0.001)
    and
    (
      rate(http_requests_total{service="order-service",status=~"5.."}[1h])
      / rate(http_requests_total{service="order-service"}[1h])
    ) > (14.4 * 0.001)
  for: 2m
  labels:
    severity: critical
    team: <team-name>
  annotations:
    summary: "OrderService error budget burning at 14.4× rate"
```

---

## 4. 錯誤預算政策（Error Budget Policy）

> 此政策說明當錯誤預算在不同水位時，團隊應採取什麼行動。

### 4.1 預算充裕（> 50% remaining）

- 正常進行功能開發與部署
- 依正常 review 流程發布變更
- 可進行非緊急效能優化

### 4.2 預算緊張（25–50% remaining）

- 暫停非必要的高風險變更
- 加強部署前測試要求（需 staging 驗證 24h 以上）
- 召開每週可靠性回顧會議
- 優先排入可靠性改善 ticket

### 4.3 預算耗盡（< 25% remaining）

- **凍結**所有功能部署（hotfix 除外）
- 啟動緊急可靠性改善 sprint
- 向產品負責人與上游消費者通知
- 每日向工程主管回報進度

### 4.4 預算耗盡（0% remaining）

- 立即召開事故回顧會議
- 評估是否需要調降 SLO 目標（需 ADR）
- 所有功能工作停止，直到預算恢復 > 25%
- 向消費者啟動 SLA 補救流程（若適用）

---

## 5. SLA 對應關係

> 如果本服務對外有合約 SLA，填寫此節；若無外部 SLA，可省略。

| 欄位 | 值 |
|---|---|
| 外部 SLA 目標 | <e.g. 99.5% per calendar month> |
| 內部 SLO 目標 | 99.9%（內部 SLO 必須高於外部 SLA） |
| 補救條款 | <e.g. 按 SLA 協議提供服務積分> |
| 量測視窗差異 | 外部 SLA 按月曆月；內部 SLO 按 30 天滾動 |
| SLA 違反流程 | 通知 `<account-manager-or-legal>` → 計算積分 → 自動開票 |

---

## 6. 儀表板與告警配置

| 資源 | 連結 / 值 |
|---|---|
| Grafana 儀表板 | `<https://grafana.example.com/d/<dashboard-id>>` |
| SLO 儀表板 | `<https://grafana.example.com/d/<slo-dashboard-id>>` |
| PagerDuty 服務 | `<service-name>` (ID: `<PXXXXXXX>`) |
| 告警路由 | Critical → on-call; Warning → `#<slack-channel>`; Info → `#sre-digest` |
| Runbook 位置 | `docs/runbooks/<service-name>.md` |
| 狀態頁面 | `<https://status.example.com>` |

### 6.1 告警抑制規則

| 情境 | 抑制條件 |
|---|---|
| 計劃性維護 | 在 PagerDuty maintenance window 期間抑制所有 non-Critical |
| 已知事故處理中 | 同一服務的 Warning 在 Critical 觸發後 15 分鐘內抑制 |
| 部署視窗 | 部署後 10 分鐘內，延遲告警閾值提升 2× |

---

## 7. 審查節奏

| 活動 | 頻率 | 參與者 | 產出 |
|---|---|---|---|
| SLO 週報 | 每週 | SRE + 服務 owner | 錯誤預算消耗趨勢報告 |
| 月度回顧 | 每月 | SRE + 服務 owner + PM | 月度 SLO 達標確認；政策調整 |
| 季度調整 | 每季 | SRE + 工程主管 | SLO 目標值重新校準；ADR（如有變更） |
| SLA 對帳 | 按月曆月 | 法務 / 帳號管理 | 外部 SLA 達標確認；積分計算（如適用） |

> **SLO 變更**：調整 SLO 目標值屬於 tier-2 contract 變更，需執行 CIA（`sunnydata-change-impact-analysis`）並寫入 ADR。

---

## See also

- `1-decisions/ARCH-0000-architecture-overview.template.md` — NFR 目標值（可用性、延遲）的來源
- `2-contracts/TM-0000-traceability-matrix.template.md` — §Non-Functional Coverage 指向此文件
- `3-process/PROC-0005-deployment-runbook.template.md` — 部署時告警配置步驟
- `3-process/PROC-0009-incident-response.template.md` — 錯誤預算耗盡時的事故回應流程
- `4-exploration/CIA-0000-change-impact-analysis.template.md` — SLO 目標變更需 CIA gate
- `.claude/rules/change-governance.md` — SLO 變更觸發 "test plan" / "architecture boundary" CIA gate
