---
id: PC-0000
title: "Page Contract"
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

# Page Contract - [專案名稱]

> **Tier**: 2-contracts — per-page contract; each page declares its own job, consumed by router + tests
>
> **Source**: realigned from `5-views/frontend-information-architecture.template.md` §6 per [ADR-0001](../1-decisions/ADR-0001-frontend-template-tier-realignment.md).

---

## 用法

每個核心頁面複製 §1 表格一份；非核心頁面（純展示型 marketing page）可省略。

頁面職責 = 合約。**變更頁面職責、資料需求或主 CTA 視為 contract change → 觸發 CIA**（依 `.claude/rules/change-governance.md`）。

---

## 1. 頁面: [名稱]

| 項目 | 內容 |
| :--- | :--- |
| **路由** | `/path` |
| **Page ID** | `PG-NNNN`（與 `FI-0000-flow-index.template.md` 對應） |
| **單一職責** | [一句話描述此頁存在的唯一目的] |
| **使用者目標** | [使用者來到此頁要完成什麼] |
| **資料需求** | API: `[GET /xxx]` / Store: `[stores/yyy]` / URL params: `[?z=...]` |
| **主要 CTA** | [primary action]，導向 `[next page]` |
| **次要行動** | [secondary actions] |
| **導航入口** | 從 `[PG-XXXX]` `[PG-YYYY]` 進入 |
| **導航出口** | 可前往 `[PG-AAAA]` `[PG-BBBB]` |
| **空狀態** | [當無資料時的設計] |
| **錯誤狀態** | [API 失敗時的設計] |
| **載入狀態** | [skeleton / spinner / streaming] |
| **權限要求** | [public / authenticated / role: admin] |
| **SEO** | title / description / OG / structured data 計畫 |

### 對應 BDD Scenario

連結到 `[feature-file].feature` 的相關 scenario（`vibecoding-write-frontend-bdd` 產出）。

### 對應測試

| Test ID | 類型 | 描述 |
| :--- | :--- | :--- |
| `TC-NNNN` | E2E | 從入口走到主 CTA 完成的 happy path |
| `TC-NNNN` | Component | 空狀態渲染 |
| `TC-NNNN` | Component | 錯誤狀態渲染 |

---

_(為每個核心頁面複製上方區塊)_

---

## 2. Sync Discipline

- 新增 / 移除頁面：必須同步更新 `5-views/VIEW-0004-frontend-route-map.template.md` 的路由表
- 修改頁面職責：必須同步更新對應 BDD feature 與 E2E 測試
- `sunnydata-doc-freshness` 會比對 `last-synced-with` 與 router config commit
