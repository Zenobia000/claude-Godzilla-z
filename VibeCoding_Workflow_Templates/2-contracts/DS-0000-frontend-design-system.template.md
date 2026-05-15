---
id: DS-0000
title: "Frontend Design System & Communication Contract"
status: draft         # draft | active | deprecated | superseded
tier: 2-contracts
owner: HYBRID (AI-drafts, human-approves)
last-reviewed: <YYYY-MM-DD>
last-synced-with: <commit-sha>
sync-source: doc      # doc | code — which side is authoritative
source-paths: []
synced-at: <YYYY-MM-DD>
product-version: null
supersedes: null
superseded-by: null
---

# Frontend Design System & Communication Contract - [專案名稱]

> **Tier**: 2-contracts — frontend design system and communication contract; consumed by frontend code
>
> **Source**: realigned from `5-views/frontend-architecture.template.md` §3+§7+§8 per [ADR-0001](../1-decisions/ADR-0001-frontend-template-tier-realignment.md).

---

## 1. 設計令牌 (Design Tokens)

| 類別 | 定義位置 | 範例值 |
| :--- | :--- | :--- |
| 色彩 | `tokens/colors.{ts,scss}` | `primary`, `secondary`, `error`, `warning`, `success` |
| 字體 | `tokens/typography` | `heading-1..6`, `body-{sm,md,lg}`, `caption`, `code` |
| 間距 | `tokens/spacing` | `xs(4)`, `sm(8)`, `md(16)`, `lg(24)`, `xl(32)`, `2xl(48)` |
| 陰影 | `tokens/shadows` | `sm`, `md`, `lg`, `focus-ring` |
| 圓角 | `tokens/radius` | `sm(4)`, `md(8)`, `lg(16)`, `full` |
| 動效 | `tokens/motion` | `duration-{fast,normal,slow}`, `easing-{in,out,inout}` |

> 變動 token 屬於 contract change → 觸發 change-governance hard gate。

## 2. 元件分層 (Atomic Design)

```
原子 (Atoms)      → Button, Input, Icon, Badge
分子 (Molecules)  → SearchBar, FormField, Card
組織 (Organisms)  → Header, Sidebar, DataTable
模板 (Templates)  → DashboardLayout, AuthLayout
頁面 (Pages)      → HomePage, LoginPage, Dashboard
```

每層的 import 規則：
- 上層可 import 下層；**下層禁止 import 上層**
- 同層元件之間 import 需書面說明（見 ADR）

---

## 3. API 通訊規範

- **統一 API Client 封裝**：禁止元件直接呼叫 `fetch` 或 `axios`，全部透過 `services/apiClient`
- **型別自動生成**：從 OpenAPI / GraphQL Schema 產生 request/response 型別（`scripts/gen-types.ts`）
- **錯誤處理**：API Client 統一捕獲 → 分類（network / 4xx / 5xx）→ Toast 或 Error Boundary 呈現
- **Retry 策略**：5xx 自動 retry 3 次（指數退避）；4xx 不 retry；網路斷線進 offline queue

## 4. 認證與授權

- **Token 儲存優先序**：httpOnly Cookie > Memory > sessionStorage（永遠不存 localStorage）
- **自動 refresh**：Access Token 過期前 30s 觸發 refresh；refresh 失敗導向 `/login`
- **路由守衛**：HOC / middleware 包裝；未授權路由回 401 page，無 silent redirect

---

## 5. 前端安全 Checklist

| 項目 | 必要 | 驗證點 |
| :--- | :--- | :--- |
| XSS 防護 | ✅ | 框架自動跳脫 + 嚴格 CSP（`script-src 'self'` 起跳）|
| CSRF 防護 | ✅ | SameSite Cookie + double-submit token |
| 敏感資料隔離 | ✅ | 禁止 localStorage 存 PII / token / API key |
| 依賴掃描 | ✅ | CI 執行 `npm audit` / `snyk`；high/critical 阻擋 merge |
| Subresource Integrity | ✅ | 所有 CDN 載入的 script/link 需 `integrity=` |
| 反爬蟲/反自動化 | 視業務 | reCAPTCHA / Cloudflare Turnstile |

---

## 6. Sync Discipline

- 每次合 PR 變更 frontend code，要回頭檢查本檔的 token / API client / auth 假設是否仍成立
- 跑 `sunnydata-doc-freshness` skill 比對 `last-synced-with` 與最新 commit；> 30 commits drift 視為 stale
