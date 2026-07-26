# Runbook - [故障情境／症狀]

> **版本:** v1.0 | **更新:** YYYY-MM-DD | **Owner:** SRE / on-call
> **原則:** 一個故障情境一份 Runbook，以症狀命名（如 `runbook-api-latency-high.md`）；寫給凌晨三點被叫醒的人看。
> **語域:** L3（工程）
> **實例:** 每故障症狀一份（`runbook-<symptom>.md`）

---

## 目錄

- [1. Symptoms（症狀）](#1-symptoms症狀)
- [2. Impact（影響）](#2-impact影響)
- [3. Possible Causes（可能原因）](#3-possible-causes可能原因)
- [4. Diagnosis（診斷步驟）](#4-diagnosis診斷步驟)
- [5. Mitigation（短期緩解）](#5-mitigation短期緩解)
- [6. Recovery（恢復確認）](#6-recovery恢復確認)
- [7. Escalation（升級路徑）](#7-escalation升級路徑)
- [8. 追溯](#8-追溯)

## 1. Symptoms（症狀）

使用者或監控會看到什麼：

- [API p95 latency > 1s]
- [Error rate > 5%]
- [對應的 alert 名稱與告警來源]

## 2. Impact（影響）

| 項目 | 內容 |
| :--- | :--- |
| **受影響功能／客戶** | |
| **嚴重程度判定** | [什麼情況升級為 incident] |

## 3. Possible Causes（可能原因）

按發生機率排序：

1. [DB connection pool 耗盡]
2. [Redis 不可用]
3. [外部 API timeout]

## 4. Diagnosis（診斷步驟）

```bash
# 每一步給具體指令或連結，不寫「檢查系統狀態」這種空話
# 1. 看 dashboard
[Grafana dashboard 連結]
# 2. 查 API log
[log 查詢指令／連結]
# 3. 查 slow query
[SQL 或工具指令]
```

## 5. Mitigation（短期緩解）

1. [Scale API pods：指令]
2. [暫時關閉不穩定的外部整合：feature flag]
3. [新版本造成的 regression → rollback：見 `deployment_and_operations.md` §6]

## 6. Recovery（恢復確認）

- [恢復服務的步驟與順序]
- [確認恢復的指標：alert 解除、p95 回到基線]

## 7. Escalation（升級路徑）

| 情況 | 找誰 | 管道 |
| :--- | :--- | :--- |
| [緩解 30 分鐘無效] | [owner／團隊] | [on-call 系統] |

---

事故結束後 48 小時內完成覆盤紀錄（正式覆盤文件依需增建）。

## 8. 追溯

| 項目 | ID |
| :--- | :--- |
| 對應告警 | [alert 名稱／來源] |
| 對應 NFR | NFR-*（可用性／延遲目標） |
| 事故紀錄 | [postmortem 連結，文件依需增建] |
