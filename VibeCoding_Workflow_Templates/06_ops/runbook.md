# Runbook - [故障情境／症狀]

> **版本:** v1.0 | **更新:** YYYY-MM-DD | **Owner:** SRE / on-call
> **原則:** 一個故障情境一份 Runbook，以症狀命名（如 `runbook-api-latency-high.md`）；寫給凌晨三點被叫醒的人看。

---

## Symptoms（症狀）

使用者或監控會看到什麼：

- [API p95 latency > 1s]
- [Error rate > 5%]
- [對應的 alert 名稱，見 `monitoring_spec.md`]

## Impact（影響）

| 項目 | 內容 |
| :--- | :--- |
| **受影響功能／客戶** | |
| **嚴重程度判定** | [什麼情況升級為 incident] |

## Possible Causes（可能原因）

按發生機率排序：

1. [DB connection pool 耗盡]
2. [Redis 不可用]
3. [外部 API timeout]

## Diagnosis（診斷步驟）

```bash
# 每一步給具體指令或連結，不寫「檢查系統狀態」這種空話
# 1. 看 dashboard
[Grafana dashboard 連結]
# 2. 查 API log
[log 查詢指令／連結]
# 3. 查 slow query
[SQL 或工具指令]
```

## Mitigation（短期緩解）

1. [Scale API pods：指令]
2. [暫時關閉不穩定的外部整合：feature flag]
3. [新版本造成的 regression → rollback：見 `deployment_and_operations.md` §6]

## Recovery（恢復確認）

- [恢復服務的步驟與順序]
- [確認恢復的指標：alert 解除、p95 回到基線]

## Escalation（升級路徑）

| 情況 | 找誰 | 管道 |
| :--- | :--- | :--- |
| [緩解 30 分鐘無效] | [owner／團隊] | [on-call 系統] |

---

事故結束後 48 小時內完成 [`incident_postmortem.md`](./incident_postmortem.md)。
