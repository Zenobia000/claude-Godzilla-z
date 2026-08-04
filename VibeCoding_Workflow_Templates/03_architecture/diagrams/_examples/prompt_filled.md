# Worked Example — 填好版生成 prompt（ACME Field Service，虛構）

> 這是 [solution_overview](../solution_overview.md) §2 依專案 SAD 填好後的樣子（few-shot 錨點）。
> 生成鏈路：**模板 §2 ＋ 專案 sad.md → 本 prompt → 宣告式 spec（[acme_solution_overview.py](./acme_solution_overview.py)）→ `.drawio`**。
> 驗收證據：`python3 ../_tools/analyze_layout.py .` → cross=0, pierce=0。

---

畫一張由左至右的端到端參考架構，抽象層級 L1 Zone＋L2 主要元件（只畫 L2）。

## L1 Zones

1. **Z1 Actors & Inbound Signals**：客戶（Web/LINE 聊天）、營運人員（後台）、外勤技師（App）；不承擔業務狀態
2. **Z2 Channel & AI Runtime**：Chat Gateway（驗簽/去重）、Assistant Runtime（對話編排/工具白名單）、Model Gateway（供應商無關路由）、Knowledge Store（vector）
3. **Z3 Interaction & Event Distribution**：REST API/ACL（認證·租戶·授權守衛）、Outbox Relay、Event Bus 🔜、Realtime Hub (WS)
4. **Z4 Domain Services & Data**：Order Service（工單/派工真相）、Billing Service、Domain DB（SQL·outbox）、Evidence Object Store
5. **Z5 Applications & External Systems**：Ops Portal、Payment Provider（外部）、Cloud Platform（外部）

底部 Cross-Cutting Management Zone：Control Plane／Configuration／Identity & Access／Security & Governance／Observability。**只用位置表達「支撐所有 zone」，不畫連線**。

## 四條語意資料路徑

| 線型 | 本專案的線 |
|---|---|
| 藍實線 | 客戶→Gateway（webhook）、Gateway→Assistant（turn）、Assistant→API（REST）、API→Order（command）、營運→Portal（HTTPS）、Portal→API（REST）、Assistant→Model Gateway、WS Hub→Portal（推送）、Billing→Payment（請款 API） |
| 綠虛線 | DB→Outbox Relay（輪詢）、Relay→Event Bus（publish 🔜）、Bus→Billing（order.completed 🔜） |
| 紫虛線 | Portal→API（租戶設定/feature flag 下發）；身分/稽核由治理帶承載不畫線 |
| 橘虛線 | Order→DB（SQL·outbox insert）、Assistant→Knowledge Store（RAG 查詢） |

## 邊界鐵律（引自本專案 ADR，示例）

- 外部整合（LLM、Payment）一律經 Gateway，不直連內部資料。
- AI（Assistant Runtime）不得直接開單、派工或觸發金流——只能經 REST API 守衛鏈。
- Event Bus 未落地，標 🔜 虛框；現況走 outbox。

## 版面決策（讓 analyze_layout score=0）

1. 長距離連線走專用通道：上方 lane y36/46/56（錯開高度）、右側外緣 x1600。
2. 同通道的線共用端點（analyzer 不計共端點交叉）；不共端點就分不同高度。
3. Z4 用「服務→儲存水平相鄰」的行列擺位，把長垂直線消除成短水平線。
4. 擦邊的線（g1 掃過 Order Service 下緣）加一個 waypoint 先下再走。
