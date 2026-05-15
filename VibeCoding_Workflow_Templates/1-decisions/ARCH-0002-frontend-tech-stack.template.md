---
id: ARCH-0002
title: "Frontend Tech Stack & Project Structure"
status: draft
tier: 1-decisions
owner: HUMAN-ONLY
last-reviewed: <YYYY-MM-DD>
date: <YYYY-MM-DD>
decider: <person-or-team>
product-version: null
supersedes: null
superseded-by: null
---
# Frontend Tech Stack & Project Structure - [專案名稱]

> **Tier**: 1-decisions — frontend framework, tooling, and project structure decisions

---

## 1. 系統化分層

```
用戶感知層    -- 視覺元件、樣式系統、動畫
互動邏輯層    -- 事件處理、表單驗證、路由
狀態管理層    -- 全局狀態、本地狀態、Server State、URL State
資料通訊層    -- API 客戶端、資料轉換、快取
基礎設施層    -- 建置工具、測試框架、監控、CI/CD
```

### 各層職責與技術選型

| 層級 | 職責 | 採用技術 | 替代選項 | 理由 |
| :--- | :--- | :--- | :--- | :--- |
| 感知層 | 渲染 UI、視覺一致性 | [React/Vue/Svelte] + [CSS Modules/Tailwind/Styled] | | |
| 互動層 | 使用者輸入、路由導航 | [React Router/Vue Router] + [React Hook Form/Formik] | | |
| 狀態層 | 狀態管理 | [Zustand/Redux/Pinia] + [React Query/SWR] | | |
| 通訊層 | API 呼叫與快取 | [Axios/fetch] + [React Query/Apollo] | | |
| 基礎設施 | 建置與品質 | [Vite/webpack] + [Jest/Vitest] + [Playwright] | | |

> 每行的「理由」欄必填，未填代表決策未完成；觸動 change-governance hard gate。

---

## 2. 專案結構

```
src/
├── assets/          # 靜態資源
├── components/      # 共用元件 (Atomic Design)
│   ├── atoms/
│   ├── molecules/
│   └── organisms/
├── features/        # 功能模組 (按功能組織)
│   └── [feature]/
│       ├── components/
│       ├── hooks/
│       ├── services/
│       └── types/
├── hooks/           # 共用 Hooks
├── layouts/         # 佈局元件
├── pages/           # 頁面路由
├── services/        # API 客戶端
├── stores/          # 狀態管理
├── styles/          # 全域樣式/Design Tokens
├── types/           # 型別定義
└── utils/           # 工具函式
```

---

## 3. 程式碼品質工具鏈

| 領域 | 工具 | 設定 |
| :--- | :--- | :--- |
| Linter | ESLint + Prettier | [.eslintrc / .prettierrc] |
| Type | TypeScript strict mode | [tsconfig.json] |
| Commit | Conventional Commits + commitlint | [.commitlintrc] |
| Branch | Git Flow / Trunk-Based | [選一] |

---

## 4. 重新評估觸發條件

- 採用的框架釋出 major 版本（如 React 19 → 20）
- 新增第 2 個前端應用（如行動 App）需要共用部分技術選型
- 既有選型已連續 2 季度成為效能瓶頸來源

觸發後應寫新 ADR supersede 本檔，不直接 in-place 改寫。