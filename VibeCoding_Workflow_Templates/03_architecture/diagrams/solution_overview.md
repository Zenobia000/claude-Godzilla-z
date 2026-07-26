# 解決方案架構總覽圖 (Solution Architecture Overview) - [專案名稱]

> **版本:** v1.0 | **更新:** YYYY-MM-DD | **狀態:** 草稿/已批准
> **Owner:** 架構師
> **語域:** L2（橋接）
> **實例:** 單例（每專案一張；多環境／future state 以分頁承載，不另開檔）
>
> **定位**：架構首頁「那一張圖」的生成規格——端到端責任分區與資料路徑語意。C4 各層圖歸 [c4_context](./c4_context.md)／[c4_container](./c4_container.md)／[sad](../sad.md) §1；視覺規範歸 [README](./README.md)。

## 目錄

- [1. 圖面資訊](#1-圖面資訊)
- [2. 生成 prompt](#2-生成-prompt)
- [3. 約束與檢查](#3-約束與檢查)
- [4. 追溯](#4-追溯)

## 1. 圖面資訊

| 欄位 | 值 |
|---|---|
| 受眾 | 主管、客戶、新人 onboarding |
| 回答的問題 | 系統端到端由哪幾個責任區組成？資料以哪幾種語意流動？ |
| 正典來源 | [sad](../sad.md)、BRD |
| 最後校驗 | YYYY-MM-DD |
| 階段 | 企業級（Pilot 前不畫——架構未穩定時必然過期） |

## 2. 生成 prompt

畫一張由左至右的端到端參考架構，抽象層級 L1 Zone＋L2 主要元件（**只畫 L2**，不畫 class、function、endpoint、table 或 UI 頁面）。

### 2.1 L1 Zones（依「訊號流入 → 處理 → 分發 → 領域真相 → 應用與外部」調整命名）

1. **Actors & Inbound Signals**：外部角色與原始訊號，不承擔業務狀態
2. **Channel & Runtime**：通道驗證、[核心處理引擎，如 AI Runtime／API Gateway]
3. **Interaction & Event Distribution**：同步 ACL、即時 fan-out、可靠外送、事件骨幹
4. **Domain Services & Data**：擁有 [核心領域物件] 真相的服務與資料
5. **Applications & External Systems**：對人操作面與外部系統整合

底部一條 **Cross-Cutting Management Zone**：Control Plane／Configuration／[通道與客戶端管理]／Security & Governance／Observability——橫切能力不混入業務主鏈。

### 2.2 四條語意資料路徑（線型固定，不得合併）

| 線型 | 語意 | 線上標註 |
|---|---|---|
| 藍色實線 | 即時互動／同步交易 | 協定或格式（webhook、REST、WebSocket…） |
| 綠色虛線 | 領域事件／非同步 metadata | Internal JSON、AsyncAPI、topic family |
| 紫色虛線 | 控制、設定、身分、安全、License | OIDC、RBAC、tenant policy、feature flag |
| 橘色虛線 | 持久化、重播與證據 | SQL、Outbox、vector store、event replay、audit |

### 2.3 視覺

白底、扁平化、低裝飾、無 3D icon。Zone 用淡色表頭與灰色邊界；Component 白底加語意色框。連線正交路由、保留獨立 lane。圖例同時說明四種線型、同步／非同步與 `🔜`。

## 3. 約束與檢查

- [ ] 所有外部整合通過明確 adapter／gateway，不直連內部資料
- [ ] 本產品的邊界鐵律逐條標上（例：[模組 A 不得直連資料庫 B]，引 ADR-*）
- [ ] 未落地能力標 `🔜`；落地狀態依 code 與部署證據判斷
- [ ] 未虛構本產品不存在的能力（元件先對照正典文件盤點再畫）
- [ ] Zone 責任表與 L2 元件目錄表放 [sad](../sad.md)（表格、不畫成圖），圖面引用之

## 4. 追溯

- 上游：[sad](../sad.md) §1–§2（系統與邊界）、相關 `ADR-*`（邊界鐵律）
- 下游：簡報／Confluence 架構首頁、onboarding 材料、[c4_container](./c4_container.md) 細化
- Worked example（虛構專案，few-shot 錨點）：[`_examples/prompt_filled.md`](./_examples/prompt_filled.md) → [spec](./_examples/acme_solution_overview.py) → `.drawio`（score=0）
