---
id: PRD-NNNN
title: "專案簡報與產品需求文件 (PRD)"
status: draft
tier: 4-exploration
owner: HYBRID
created: <YYYY-MM-DD>
target-release: <version-or-quarter>
product-version: null
supersedes: null
superseded-by: null
---
# 專案簡報與產品需求文件 (PRD) - [專案名稱]

> **Tier**: 4-exploration — product requirements document for feature scoping and planning

---

## 1. 專案總覽

| 項目 | 內容 |
| :--- | :--- |
| **專案名稱** | [專案代號/名稱] |
| **狀態** | [規劃中 / 開發中 / 已上線] |
| **目標發布日期** | YYYY-MM-DD |
| **核心團隊** | PM: / Lead Engineer: / UX: |

---

## 2. 商業目標

| 項目 | 內容 |
| :--- | :--- |
| **背景與痛點** | [當前問題、影響範圍] |
| **策略契合度** | [如何支持公司戰略目標] |
| **成功指標** | 主要: [KPI 1] / 次要: [KPI 2] |

---

## 3. 使用者故事與允收標準

### Epic: [例如：使用者身份驗證]

| ID | 描述 (As a / I want to / So that) | 允收標準 | BDD 連結 |
| :--- | :--- | :--- | :--- |
| US-001 | As a 新使用者, I want to 透過 Email 註冊, so that 我可以使用服務。 | 1. 有效 Email 註冊成功 2. 收到驗證信 3. 驗證後帳號啟用 | `auth.feature` |
| US-002 | | | |

---

## 4. 範圍與限制

| 項目 | 內容 |
| :--- | :--- |
| **功能範圍** | - [模組 A] - [模組 B] |
| **非功能需求** | 性能: [需求] / 安全: [需求] / 可用性: [需求] |
| **不做什麼** | - [明確排除項 1] |
| **假設與依賴** | 假設: [項目] / 依賴: [外部服務] |

---

## 5. 待辦問題與決策

| ID | 描述 | 狀態 | 負責人 |
| :--- | :--- | :--- | :--- |
| Q-001 | [待澄清問題] | 待討論 | |
| D-001 | [已做決策] | 已決定 | |

---

## 6. 前端資訊架構概覽（前端產品適用）

> 本章節僅描述「使用者體驗的意圖」；技術選型見 `1-decisions/ARCH-0002-frontend-tech-stack.template.md`，頁面合約見 `2-contracts/PC-0000-page-contract.template.md`，路由樹見 `5-views/VIEW-0004-frontend-route-map.template.md`。

### 6.1 核心價值主張

> 「[一句話描述為使用者提供的核心價值]」

### 6.2 資訊架構原則

| 原則 | 說明 |
| :--- | :--- |
| 簡化 | 保留: [核心功能] / 移除: [排除功能] / 專注: [聚焦點] |
| 認知負荷 | 每頁 1 個主要目標，先總覽再深入 |
| 架構模式 | [ ] 扁平化 / [ ] 層級化 / [ ] 中心輻射 / [ ] 混合 |

### 6.3 核心使用者旅程

```mermaid
graph LR
    A[階段1] --> B[階段2] --> C[階段3] --> D[階段4]
```

| 階段 | 頁面 (PG-*) | 使用者心理 | 設計目標 | 主要 CTA | 轉換率目標 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [階段名] | `[PG-NNNN]` | [心理描述] | [目標] | [CTA] | [%] |