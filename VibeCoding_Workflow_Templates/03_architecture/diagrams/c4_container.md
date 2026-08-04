# 容器圖 (C4 Container) - [專案名稱]

> **版本:** v1.0 | **更新:** YYYY-MM-DD | **狀態:** 草稿/已批准
> **Owner:** 架構師
> **語域:** L2（橋接）
> **實例:** 單例（每專案一張；多環境／future state 以分頁承載，不另開檔）
>
> **定位**：C4 L2 全景主錨圖溝通級 drawio 版的生成規格；與 [sad](../sad.md) §1.2 mermaid 二擇一，不得雙軌維護。容器內部（L3）歸 sad §1.3 mermaid；部署實體化歸 [deployment_topology](./deployment_topology.md)。

## 目錄

- [1. 圖面資訊](#1-圖面資訊)
- [2. 生成 prompt](#2-生成-prompt)
- [3. 約束與檢查](#3-約束與檢查)
- [4. 追溯](#4-追溯)

## 1. 圖面資訊

| 欄位 | 值 |
|---|---|
| 受眾 | 跨團隊對接、新進工程師（團隊的共同語言） |
| 回答的問題 | 系統內有哪些可獨立部署／執行的 runtime？彼此怎麼連？ |
| 正典來源 | [sad](../sad.md) §1.2 |
| 最後校驗 | YYYY-MM-DD |
| 階段 | 雛型起（雛型期用 sad mermaid 即可；對外溝通時轉 drawio） |

## 2. 生成 prompt

畫 C4 Container 全景圖：actor＋全部 runtime 單位＋主要連線。方塊**必須是 runtime**：

| 類別 | 內容 | 形狀／配色 |
|---|---|---|
| 應用程序 | [web 前台 :port]／[api 服務 :port]／[worker／agent] | 圓角矩形、依語意配色 |
| 資料儲存 | [主資料庫]／[快取]／[向量庫] | 圓柱 |
| 共用服務 | [身分供應商]／[可觀測平台]／[事件骨幹] | 綠 |
| 獨立子系統 | [子系統名]，內部只列自己的 runtime | 青色 container 框 |

部署邊界用 container／swimlane 分組（例：可獨立部署單元 × 集中共用平台 × 附加模組——依專案實際拓撲，不硬套三分）。

## 3. 約束與檢查

- [ ] 無 module／package 當容器、無「資料平面」「邏輯層」等抽象元素
- [ ] 每條跨邊界連線標協定與用途；主鏈粗實線、回流虛線、橫切點線
- [ ] 每個 Container 標 L3 揭露狀態（✅ 有圖／表代圖／略，附理由）
- [ ] 環境間拓撲不對稱（本機 vs 雲端缺件）已註記，不隱藏
- [ ] 有 milestone 時 future state 另畫獨立一張，不只在當前圖打虛線；單一元件未落地才用 `🔜`
- [ ] 圖例＋metadata banner 已附

## 4. 追溯

- 上游：[sad](../sad.md) §1.2（Container 清單與技術）、`ADR-*`（部署邊界決策）
- 下游：[deployment_topology](./deployment_topology.md)、[sad](../sad.md) §1.3 各 L3 圖
