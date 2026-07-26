# 事件規格 (Event Spec) - [事件／通道名稱]

> **版本:** v1.0 | **更新:** YYYY-MM-DD | **狀態:** 草稿/審核中/已批准
> **Owner:** 後端 / 平台
> **適用時機:** 使用 Kafka / RabbitMQ / PubSub 等非同步通道時；純同步 API 只需 `api_spec.md`。

---

## 1. 事件定義

| 項目 | 內容 |
| :--- | :--- |
| **eventType** | `work_order.assigned` |
| **eventVersion** | 1.0 |
| **topic / queue** | `work-order-events` |
| **producer** | [dispatch-service] |
| **consumers** | [notification-service、analytics-service] |
| **觸發時機** | [業務事件的精確定義；對應狀態機轉移] |

---

## 2. Schema

Schema 的 SSOT 是 [`asyncapi.yaml`](./asyncapi.yaml)（複製後改名 `asyncapi-<domain>-v<N>.yaml`）；以下為說明用示例。

```json
{
  "eventId": "uuid",
  "eventType": "work_order.assigned",
  "eventVersion": "1.0",
  "occurredAt": "ISO-8601",
  "payload": {
    "workOrderId": "uuid",
    "assigneeId": "uuid"
  }
}
```

| 欄位 | 必填 | 說明 |
| :--- | :--- | :--- |
| `eventId` | ✓ | 冪等鍵（idempotency key） |
| `payload.workOrderId` | ✓ | 排序鍵（ordering key） |

---

## 3. 傳遞語意

| 項目 | 政策 |
| :--- | :--- |
| **Ordering** | by `workOrderId`（同一工單事件有序） |
| **Delivery** | at-least-once；consumer 必須冪等 |
| **Retry** | exponential backoff，max [3] 次 |
| **DLQ** | `work-order-events-dlq`；處理流程見 Runbook |
| **Schema 演進** | 只允許向後相容變更；破壞性變更升 major version 並雙軌發布 |

---

## 4. 消費者契約

| Consumer | 關心的欄位 | 失敗行為 | 冪等策略 |
| :--- | :--- | :--- | :--- |
| notification-service | payload.assigneeId | [重試 / 進 DLQ] | [以 eventId 去重] |

---

## 5. 追溯

- 觸發來源：狀態機轉移（`sds.md` §狀態機）
- 監控：lag 與 DLQ 深度告警見 `../06_ops/monitoring_spec.md`
