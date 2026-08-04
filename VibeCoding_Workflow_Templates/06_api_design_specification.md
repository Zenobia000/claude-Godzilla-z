# API 設計規範 - [API/服務名稱]

> **版本:** v1.0 | **更新:** YYYY-MM-DD | **狀態:** 草稿/已發布 | **OpenAPI 定義:** [連結]

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

---

## 3. 錯誤處理

```json
{
  "error": {
    "type": "invalid_request_error",
    "code": "parameter_missing",
    "message": "缺少必要參數 email",
    "param": "email",
    "request_id": "req_xxx"
  }
}
```

| 錯誤碼 | HTTP | 描述 |
| :--- | :--- | :--- |
| `resource_not_found` | 404 | 資源不存在 |
| `parameter_invalid` | 400 | 參數格式無效 |
| `parameter_missing` | 400 | 缺少必要參數 |
| `authentication_failed` | 401 | 認證失敗 |
| `permission_denied` | 403 | 無權限 |
| `rate_limit_exceeded` | 429 | 超出速率限制 |
| `internal_server_error` | 500 | 伺服器錯誤 |

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

---

## 7. 合約測試與版本演進

契約是對外承諾，改壞了不是 bug 是違約。這一段填不出來，代表這份 API spec 還不能對外發布。

| 項目 | 內容 |
| :--- | :--- |
| **相容性規則** | 哪些變更算 backward compatible（可直接發）／breaking（需新版本）？ |
| **版本策略** | 版本放 URL、標頭還是 Schema？棄用流程與公告期多長？ |
| **合約測試** | Provider／Consumer 各自的驗證腳本放哪、由哪個 CI 階段強制？ |
| **錯誤分類** | 哪些錯誤可重試、哪些不可？重試的冪等性由誰保證？ |
| **稽核欄位** | who／when／why 三個欄位是否都有？ |

### 蘇格拉底檢核

- 消費端在**不改任何程式碼**的前提下，能承受這次變更嗎？答不出來就是 breaking change。
- 這個錯誤碼，消費端拿到之後**知道要做什麼**嗎？還是只能重試然後放棄？
- 若這個端點被呼叫兩次（網路重送），結果一樣嗎？
