# 軟體需求規格書 (SRS) - [專案名稱]

> **版本:** v1.0 | **更新:** YYYY-MM-DD | **狀態:** 草稿/審核中/已批准
> **Owner:** SA / PM / BA，工程師與 QA 共同審閱
> **適用時機:** 需求複雜、角色權限多、整合多、需要正式驗收時；MVP 可由 PRD + BDD 承接。
> **語域:** L2（橋接）
> **實例:** 單例（整個系統一份）

---

## 目錄

- [1. 功能需求 (Functional Requirements)](#1-功能需求-functional-requirements)
- [2. 非功能需求 (NFR)](#2-非功能需求-nfr)
- [3. 資料需求 (Data Requirements)](#3-資料需求-data-requirements)
- [4. 外部介面 (External Interfaces)](#4-外部介面-external-interfaces)
- [5. 使用案例 (Use Case Specification)](#5-使用案例-use-case-specification)
- [6. 驗收標準 (Acceptance Criteria)](#6-驗收標準-acceptance-criteria)
- [7. 追溯](#7-追溯)

## 1. 功能需求 (Functional Requirements)

| ID | 需求描述 | 來源 | 優先級 | 驗收標準 ID |
| :--- | :--- | :--- | :--- | :--- |
| FR-001 | [系統應…，用可觀察行為描述] | REQ/DEC-* | Must | ACPT-001 |
| FR-002 | | | Should | |

---

## 2. 非功能需求 (NFR)

量化指標與驗證方法維護在本表與 [`../03_architecture/sad.md`](../03_architecture/sad.md) §2 非功能性需求段；獨立 NFR 文件依需增建。

| ID | 類別 | 適用範圍 |
| :--- | :--- | :--- |
| NFR-001 | 效能 | [API p95 < X ms 適用的端點] |

---

## 3. 資料需求 (Data Requirements)

| 資料實體 | 來源系統 | 保留政策 | 敏感等級 |
| :--- | :--- | :--- | :--- |
| [工單] | [本系統] | [N 年] | [含個資與否] |

---

## 4. 外部介面 (External Interfaces)

| 介面 | 方向 | 協議 | 契約文件 |
| :--- | :--- | :--- | :--- |
| [金流服務] | 出 | REST | `../04_design/api_spec.md` |

---

## 5. 使用案例 (Use Case Specification)

> 流程複雜、例外多或稽核需求高時才展開；一般功能用 User Story + BDD 即可。

### UC-001: [案例名稱]

| 項目 | 內容 |
| :--- | :--- |
| **Actor** | [角色] |
| **Preconditions** | [前置條件] |
| **Main Flow** | 1. … 2. … 3. … |
| **Alternative Flow** | A1. [分支條件與步驟] |
| **Postconditions** | [完成後的系統狀態] |
| **引用規則** | BR-*（見 [`brd.md`](./brd.md)） |

---

## 6. 驗收標準 (Acceptance Criteria)

AC 是需求與測試之間的橋，用 Given / When / Then 撰寫並落在 [`prd.md`](./prd.md) 的 ACPT 段（或依需增建的 feature 檔）；此處維護對照表。

| ACPT ID | 對應 FR | Scenario（SCN-*） | 狀態 |
| :--- | :--- | :--- | :--- |
| ACPT-001 | FR-001 | SCN-001 | 待驗證 |

## 7. 追溯

| 項目 | ID |
| :--- | :--- |
| 上游 | prd 的 US-*／FR-*、DEC-* |
| 本文件產出 | 正式 FR/NFR 編號、UC-*、AC 對照 |
| 下游 | sad §4 需求摘要、test_plan／uat_plan、`engineering_tracker.xlsx` ①規格追溯 |
