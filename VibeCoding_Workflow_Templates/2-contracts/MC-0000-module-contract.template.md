---
id: MC-NNNN
title: "Module Contract Template"
status: draft        # draft | active | deprecated | superseded | archived
tier: 2-contracts
owner: HYBRID (AI-drafts, human-approves)
last-reviewed: <YYYY-MM-DD>
last-synced-with: <git-commit-sha>
sync-source: code             # module contracts usually mirror code
source-paths:
  - src/<module>/
synced-at: <YYYY-MM-DD>
product-version: null
supersedes: null
superseded-by: null
---
# 模組規格與測試案例 - [模組名稱]

> **Tier**: 2-contracts — module specification and test cases; must stay synced with code

**對應架構文件**: [連結]
**對應 BDD Feature**: [連結]

---

## 模組: [名稱，例如：ShoppingCartService]

### 規格: [函式名稱，例如：AddItemToCart]

**描述**: [簡述功能]

**契約式設計 (DbC)**:

| 類型 | 條件 |
| :--- | :--- |
| **前置條件** | 1. [條件 1] 2. [條件 2] |
| **後置條件** | 1. [條件 1] 2. [條件 2] |
| **不變性** | 1. [條件 1] 2. [條件 2] |

---

### 測試案例

#### TC-001: 正常路徑

- **Arrange**: [建立初始狀態]
- **Act**: [執行操作]
- **Assert**: [驗證 1] / [驗證 2]

#### TC-002: 邊界情況

- **Arrange**: [建立邊界狀態]
- **Act**: [執行操作]
- **Assert**: [驗證結果]

#### TC-003: 無效輸入 (違反前置條件)

- **Arrange**: [建立狀態]
- **Act**: [傳入無效參數]
- **Assert**: 預期拋出 [ExceptionType]

#### TC-004: 業務規則

- **Arrange**: [建立業務極限狀態]
- **Act**: [觸發業務規則]
- **Assert**: 預期拋出 [BusinessRuleException]

---

### 更多規格...

_(複製上方結構，為每個函式/方法建立規格與測試案例)_