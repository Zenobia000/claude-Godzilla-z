# 部署拓撲圖 (Deployment Topology) - [專案名稱]

> **版本:** v1.0 | **更新:** YYYY-MM-DD | **狀態:** 草稿/已批准
> **Owner:** 架構師
> **語域:** L2（橋接）
> **實例:** 單例（每專案一張；多環境／future state 以分頁承載，不另開檔）
>
> **定位**：部署與租戶邊界溝通圖的生成規格——L2 Container 的**物理實體化**，不是把 L2 圖換底色重畫。邏輯容器歸 [c4_container](./c4_container.md)；部署程序與環境設定歸 [deployment_and_operations](../../06_ops/deployment_and_operations.md)。

## 目錄

- [1. 圖面資訊](#1-圖面資訊)
- [2. 生成 prompt](#2-生成-prompt)
- [3. 約束與檢查](#3-約束與檢查)
- [4. 追溯](#4-追溯)

## 1. 圖面資訊

| 欄位 | 值 |
|---|---|
| 受眾 | 維運、SRE、客戶技術窗口 |
| 回答的問題 | 什麼跟什麼部署在一起？哪些每客戶一套、哪些集中共用？ |
| 正典來源 | [sad](../sad.md) §7、[deployment_and_operations](../../06_ops/deployment_and_operations.md) |
| 最後校驗 | YYYY-MM-DD |
| 階段 | Pilot 起 |

## 2. 生成 prompt

畫部署拓撲：每個 logical Container instantiate 到具體 Node。常見三分模式（依專案調整，不硬套）：

| 分組 | 內容 | 配色 |
|---|---|---|
| ① 可獨立部署單元 | [per-tenant／per-instance bundle：app、db、cache…]；標註「不依賴共享元件即可自成一套上線」是否成立（引 ADR-*） | 藍 |
| ② 集中共用平台 | [身分、可觀測、跨租戶服務、管理 console] | 綠 |
| ③ 可選附加模組 | [License 加購／feature-gated 子系統] | 青 |

## 3. 約束與檢查

- [ ] 每個 Node 標屬性：OS／規格／port／scaling；每個 instance 標數量（×1、×N per tenant）
- [ ] 只畫重點跨組連線（OIDC、遙測、跨系統 API、資料回流），依語意線型，不畫滿
- [ ] 資料隔離模型明確標註（物理隔離／schema 隔離／tenant_id 邏輯隔離），引 ADR-*
- [ ] 當前與目標環境不同時各畫一張或以 `🔜` 標差異；不把目標狀態畫成現況
- [ ] 圖例＋metadata banner 已附

## 4. 追溯

- 上游：[sad](../sad.md) §7（部署視圖）、[c4_container](./c4_container.md)、`ADR-*`（隔離與拓撲決策）
- 下游：[deployment_and_operations](../../06_ops/deployment_and_operations.md)、[runbook](../../06_ops/runbook.md)、客戶技術簡報
