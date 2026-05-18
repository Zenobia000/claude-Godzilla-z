---
id: API-NNNN
title: "API Spec — REST / Async / Errors / Idempotency"
status: active
tier: 2-contracts
owner: HYBRID
essence: bedrock
absorbs: [ERR-0000-error-envelope, ASYNC-0000-async-api]
last-reviewed: null
last-synced-with: null
sync-source: doc
source-paths: ["docs/2-contracts/api/openapi.yaml", "docs/2-contracts/api/asyncapi.yaml"]
synced-at: null
product-version: null
supersedes: null
superseded-by: null
---
# API-NNNN: API Spec — REST + Async + Errors + Idempotency

> **Tier**: 2-contracts · **Essence**: bedrock — the wire contract.
>
> **One spec, REST + Async + Errors + Idempotency** — every wire surface lives here. The canonical machine-readable form is `openapi.yaml` (REST) + `asyncapi.yaml` (events); this markdown documents conventions, decisions, and error catalog.

---

## 1. 設計約定

| 項目 | 規範 |
| :--- | :--- |
| **風格** | RESTful |
| **Base URL** | Production: `https://api.example.com/v1` / Staging: `https://staging-api.example.com/v1` |
| **格式** | `application/json` (UTF-8) |
| **資源路徑** | 小寫、連字符、複數 (e.g., `/user-profiles`) |
| **欄位命名** | `snake_case` |
| **日期格式** | ISO 8601 UTC (e.g., `2023-10-27T10:00:00Z`) |
| **認證** | OAuth 2.0, Bearer Token in `Authorization` header |
| **版本控制** | URL 路徑 (`/v1/...`) |

---

## 2. 通用行為

### 分頁
游標分頁: `limit` (預設 25, 最大 100) + `starting_after` / `ending_before`

### 排序
`sort_by=field` (升序) / `sort_by=-field` (降序)

### 過濾
欄位名直接作為參數: `/users?status=active&created_at[gte]=2023-01-01`

### 冪等性

非 GET 請求可傳 `Idempotency-Key` header，伺服器 24h 內對同 key 返回相同結果。

**完整規範（L3.2 行為契約）**：
- Header `Idempotency-Key: <client-generated-ulid>`，每筆 POST/PUT/PATCH 必帶。
- 伺服器以 `(tenant_id, idempotency_key)` 為主鍵儲存 24h；相同 key + 相同 payload → 回 cached response；相同 key + 不同 payload → 回 `409 IDEMPOTENCY_KEY_CONFLICT`（見 `ERR-0000`）。
- 儲存表 schema 範例：`webhook_idempotency (tenant_id, key, request_hash, response_body, created_at)`，TTL 24h。
- Schemathesis 重放測試（`CIG-0004`）強制驗證上述行為。

詳見 [`PRIN-0003-engineering-contract-stack.md` §L3.2](../0-principles/PRIN-0003-engineering-contract-stack.md) 與 `ERR-0000-error-envelope.template.md`。

<a id="idempotency"></a>

---

## 3. 錯誤處理

> **完整規範請參考** `ERR-0000-error-envelope.template.md`（L1.3 — wire / error）。
> 本節為摘要 + 範例；envelope 的權威 schema 與 error-code registry 在 ERR-0000 維護。

範例（推薦升級到 RFC 7807 Problem Details — 見 ERR-0000）：

```json
{
  "type": "https://errors.example.com/parameter-missing",
  "title": "Parameter missing",
  "status": 400,
  "code": "PARAMETER_MISSING",
  "detail": "缺少必要參數 email",
  "errors": [{ "path": "body.email", "message": "required" }],
  "trace_id": "01HW3KQXJ2YQ7CGFD2GMXP9R5Q"
}
```

ERR-0000 §3 維護完整的 error-code closed set。任何新錯誤碼變更需同時更新：
1. ERR-0000 §3 表格
2. `messages/{locale}.json`（i18n key `error.<code>`）— 由 `CIG-0005` 強制
3. Schemathesis 測試覆蓋（`CIG-0004`）

---

## 4. 安全性

- **TLS**: 強制 HTTPS (TLS 1.2+)
- **速率限制**: 基於 API Key/User ID，回應含 `RateLimit-Limit/Remaining/Reset` headers
- **安全 Headers**: HSTS, CSP, X-Content-Type-Options
- **OWASP API Top 10**: 已考量並緩解

---

## 5. API 端點定義

### 資源: [資源名稱]

**路徑:** `/resources`

#### `POST /resources` - 建立

- **授權**: `resources.write`
- **請求體**: `ResourceCreate`
- **回應**: `201 Created` -> `Resource`

#### `GET /resources/{id}` - 取得

- **授權**: `resources.read`
- **回應**: `200 OK` -> `Resource`

#### `GET /resources` - 列表

- **授權**: `resources.read`
- **參數**: `limit`, `starting_after`, `sort_by`, `status`
- **回應**: `200 OK` -> `{ data: Resource[], has_more: boolean }`

#### `PATCH /resources/{id}` - 更新

- **授權**: `resources.write`
- **請求體**: `ResourceUpdate` (部分更新)
- **回應**: `200 OK` -> `Resource`

#### `DELETE /resources/{id}` - 刪除

- **授權**: `resources.write`
- **回應**: `204 No Content`

---

## 6. 資料模型

### `Resource`

```json
{
  "id": "string (res_...)",
  "object": "resource",
  "name": "string",
  "status": "active | inactive",
  "created_at": "string (ISO 8601)",
  "updated_at": "string (ISO 8601)"
}
```

### `ResourceCreate`

```json
{
  "name": "string (required)",
  "status": "string (optional, default: active)"
}
```

### `Problem` (RFC 7807 error envelope, absorbs ERR-0000)

```json
{
  "type":      "https://errors.example.com/<code-slug>",
  "title":     "Short human-readable summary (English; do NOT i18n at this layer)",
  "status":    400,
  "code":      "VALIDATION_FAILED",
  "detail":    "Optional free-form description (no PII)",
  "instance":  "/orders",
  "errors":    [{ "path": "body.email", "message": "required" }],
  "trace_id":  "01HW3KQXJ2YQ7CGFD2GMXP9R5Q"
}
```

**Error-code registry (closed set; AI must not invent new codes without CR):**

| code | HTTP | i18n key |
|---|---|---|
| `VALIDATION_FAILED` | 400 | `error.VALIDATION_FAILED` |
| `IDEMPOTENCY_KEY_REQUIRED` | 400 | `error.IDEMPOTENCY_KEY_REQUIRED` |
| `IDEMPOTENCY_KEY_CONFLICT` | 409 | `error.IDEMPOTENCY_KEY_CONFLICT` |
| `UNAUTHENTICATED` | 401 | `error.UNAUTHENTICATED` |
| `PERMISSION_DENIED` | 403 | `error.PERMISSION_DENIED` |
| `RESOURCE_NOT_FOUND` | 404 | `error.RESOURCE_NOT_FOUND` |
| `CONFLICT` | 409 | `error.CONFLICT` |
| `RATE_LIMITED` | 429 | `error.RATE_LIMITED` |
| `INTERNAL_ERROR` | 500 | `error.INTERNAL_ERROR` |
| `SERVICE_UNAVAILABLE` | 503 | `error.SERVICE_UNAVAILABLE` |

Rules:
- New code → CR + i18n key in every locale + Schemathesis coverage (`CIG-0005`, `CIG-0004` enforce)
- Codes are immutable; rename = deprecate + add new
- 5xx MUST NOT leak stack trace into `detail`

---

## 7. Async API (absorbs ASYNC-0000)

> Use when the service emits / consumes events (Kafka / RabbitMQ / SQS / WebSocket / Webhook / SSE). Canonical machine-readable form: `asyncapi.yaml` (AsyncAPI 2.6+); CloudEvents 1.0 envelope.

### 7.1 Per-channel contract

| Field | Example |
|---|---|
| Channel name | `orders.created` |
| Protocol | Kafka 3.6 / topic=`orders.created` / 12 partitions |
| Partition key | `order_id` (per-entity ordering) |
| Direction | producer / consumer / bidirectional |
| Delivery | `at-least-once` / `at-most-once` / `exactly-once` |
| Ordering | `per-partition` / `global` / `none` |

### 7.2 CloudEvents envelope (required for every event)

```yaml
specversion: "1.0"
type: "com.example.orders.created.v1"
source: "/services/orders"
subject: "order/{order_id}"
id: "<ULID>"
time: "<RFC 3339>"
datacontenttype: "application/json"
data: { <payload schema> }
```

### 7.3 Producer contract (per emitting service)

| Property | Rule |
|---|---|
| Emission trigger | After successful DB commit (transactional outbox; see `DATA-NNNN §migration`) |
| Retry on broker fail | 3× exponential backoff; then outbox table |
| Schema evolution | Backward-compatible only; new fields optional |

### 7.4 Consumer contract (per consuming service)

| Property | Rule |
|---|---|
| Delivery semantic | At-least-once → consumer MUST be idempotent (§2 idempotency) |
| Max processing time | 30s; beyond → DLQ |
| DLQ | `<channel>.dlq` retention 14d; manual replay via `PROC-0002 §incident` |
| Lag SLO | p99 < 60s (track in `SRE-NNNN`) |

### 7.5 Failure modes

| Mode | Detection | Mitigation |
|---|---|---|
| Broker unreachable | Local outbox grows | Read from outbox on retry; alert > 5min |
| Consumer crash mid-processing | At-least-once redelivery | Consumer-side `Idempotency-Key` (DB unique on `event_id`) |
| Schema break | `CIG-0003` blocks PR | — |
| Poison message | DLQ count > 0 | `PROC-0002 §incident` |

### 7.6 Anti-patterns

- Reusing REST DTO as event payload → couples wire to internal model → define `<Entity>Created.v1` independently
- No partition key → multi-consumer races on same entity
- At-least-once + non-idempotent consumer → duplicate processing in prod
- Webhook without HMAC signature + replay window → spoofing risk

---

## See also

- `PRIN-0003-engineering-contract-stack.md` §L1 (wire layer) + §AI.1 (prompt input)
- `MC-0000-module-contract.template.md` — module DbC consuming this API
- `DATA-0000-data-contract.template.md` §migration — schema changes affecting `Resource`
- `SRE-0000-reliability.template.md` — SLO + observability for this API
- `TEST-0000-testing-strategy.template.md` §contract — Schemathesis + Pact
- `3-process/ci-gates/CIG-0001..0005` — spec lint, types sync, asyncapi validate, schemathesis, i18n keys