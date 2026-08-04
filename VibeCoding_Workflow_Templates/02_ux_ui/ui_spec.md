# UI 規格書 (UI Spec) - [頁面／功能名稱]

> **版本:** v1.0 | **更新:** YYYY-MM-DD | **狀態:** 草稿/審核中/已批准
> **Owner:** UI / PM / Frontend 三方確認
> **回答的問題:** 每個畫面有哪些區塊、欄位、狀態、操作與文案？前端不用猜。
> **語域:** L3（工程）
> **實例:** 每頁面一份（`ui_spec-<page>.md`）

---

## 目錄

- [1. 頁面目的 (Page Purpose)](#1-頁面目的-page-purpose)
- [2. 版面配置 (Layout)](#2-版面配置-layout)
- [3. 欄位與元件 (Fields / Components)](#3-欄位與元件-fields--components)
- [4. 使用者操作 (Actions)](#4-使用者操作-actions)
- [5. UI 狀態 (States)](#5-ui-狀態-states)
- [6. 互動規格 (Interaction Spec)](#6-互動規格-interaction-spec)
- [7. 驗證規則 (Validation)](#7-驗證規則-validation)
- [8. 響應式與無障礙 (Responsive / A11y)](#8-響應式與無障礙-responsive--a11y)
- [9. 設計交付 (Design Handoff)](#9-設計交付-design-handoff)
- [10. 追溯](#10-追溯)

## 1. 頁面目的 (Page Purpose)

[一句話：這頁讓誰完成什麼任務。對應 User Flow 節點：`ux_research_and_journey.md` §5]

| 導航 | 頁面 |
| :--- | :--- |
| 入口（從哪些頁面進入） | [頁面清單，對應 `information_architecture.md` §1] |
| 出口（可前往哪些頁面） | [頁面清單] |

## 2. 版面配置 (Layout)

```text
Header / Filter Bar / Table / Pagination
```

[低保真 wireframe 連結或 ASCII 區塊圖；高保真設計稿見 §9 Handoff]

## 3. 欄位與元件 (Fields / Components)

| 欄位 | 型態 | 來源（API 欄位） | 顯示規則 |
| :--- | :--- | :--- | :--- |
| [工單編號] | text | `workOrder.id` | [格式、截斷、排序] |

## 4. 使用者操作 (Actions)

| 操作 | 觸發 | 結果 | 權限 |
| :--- | :--- | :--- | :--- |
| [新增工單] | [按鈕] | [開啟表單 Modal] | [角色] |

## 5. UI 狀態 (States)

每頁至少定義以下狀態的畫面與文案；缺一個，前端就會自己發明一個。

| 狀態 | 呈現 | 文案 |
| :--- | :--- | :--- |
| Loading | [skeleton / spinner] | |
| Empty | [空狀態插圖＋引導] | [「今天沒有指派工單」] |
| Error | [重試入口] | |
| Permission Denied | | |
| Success | [toast / inline] | |

## 6. 互動規格 (Interaction Spec)

| 元素 | Hover | Disabled | Loading | 錯誤反應 |
| :--- | :--- | :--- | :--- | :--- |
| [送出按鈕] | | [何時 disabled] | [防重複點擊] | |

## 7. 驗證規則 (Validation)

| 欄位 | 規則 | 錯誤訊息 | 觸發時機 |
| :--- | :--- | :--- | :--- |
| [地址] | 必填 | [具體文案] | [blur / submit] |

## 8. 響應式與無障礙 (Responsive / A11y)

- **斷點行為:** [Desktop 用 Table；Mobile 改 Card List]
- **鍵盤操作:** [Tab 順序、Enter/Escape 行為]
- **ARIA / 對比 / Focus:** [適用的檢查項與標準，如 WCAG 2.1 AA、對比 ≥ 4.5:1]

## 9. 設計交付 (Design Handoff)

| 項目 | 連結／位置 |
| :--- | :--- |
| Figma | [frame 連結，標注哪個 frame 是 SSOT] |
| Design Tokens | [tokens 檔或 Design System 章節] |
| 元件對照 | [Figma 元件 ↔ 程式元件名] |
| 已知限制 | [設計與實作的已知落差] |

## 10. 追溯

| 項目 | ID |
| :--- | :--- |
| 對應需求 | FR-* |
| 對應情境 | SCN-*（BDD） |
| 對應元件規格 | [Figma Design System 或程式元件庫位置；獨立前端技術設計文件依需增建] |
