# 架構圖模板手冊 (Diagram Templates Manual)

> **版本:** v1.0 | **更新:** 2026-07-26 | **狀態:** 活躍
> **Owner:** 模板庫維護者
> **語域:** L2（橋接）
>
> **定位**：drawio「對外溝通級大圖」的載體分工、視覺規範與階段裁剪。單張圖的生成規格歸本資料夾各模板；工程細圖的 mermaid 正典歸 [sad](../sad.md)／[lld](../../04_design/lld.md)。

## 目錄

- [1. 載體分工（單一 owner）](#1-載體分工單一-owner)
- [2. 階段裁剪](#2-階段裁剪)
- [3. 圖面 metadata banner](#3-圖面-metadata-banner)
- [4. 全域視覺規範](#4-全域視覺規範)
- [5. 生成管線（_tools）與範例（_examples）](#5-生成管線_tools與範例_examples)
- [6. style 字串庫](#6-style-字串庫)
- [7. 通則](#7-通則)
- [8. 追溯](#8-追溯)

## 1. 載體分工（單一 owner）

每個模板是一份**生成 prompt 規格**（可貼給 draw.io AI／Copilot，或當人工繪製規格），不是成品圖。成品 `.drawio` 是可編輯正典，匯出 SVG／PNG 嵌入文件或簡報。

| 視圖 | 正典載體 | 所在 |
|---|---|---|
| Solution Architecture Overview | **drawio** | [solution_overview](./solution_overview.md) |
| C4 L1 System Context | **drawio 或 sad mermaid，二擇一** | [c4_context](./c4_context.md)／[sad](../sad.md) §1.1 |
| C4 L2 Container | **drawio 或 sad mermaid，二擇一** | [c4_container](./c4_container.md)／[sad](../sad.md) §1.2 |
| Deployment Topology | **drawio** | [deployment_topology](./deployment_topology.md) |
| AI Guardrails Boundary（可選） | **drawio** | [ai_guardrails](./ai_guardrails.md) |
| C4 L3 Component | mermaid | [sad](../sad.md) §1.3 |
| Sequence／Dynamic | mermaid | [sad](../sad.md) §5 |
| 跨系統資料流 | mermaid | [sad](../sad.md) §6 |
| ER 圖 | mermaid | [db_design](../../04_design/db_design.md) |
| State Machine | mermaid | [lld](../../04_design/lld.md) §5 |

選擇基準：mermaid 活在文件內、可 diff、可 review、隨 code 走，是工程正典；drawio 版面品質高但 diff 不了、維護貴，只留給「半年後還有人點開」的大圖。同一視圖若上了 drawio，文件對應段落改放匯出圖連結，**不得雙軌維護**。

## 2. 階段裁剪

| 階段 | 需要的圖 |
|---|---|
| 雛型（Prototype） | Context＋Container（sad 內 mermaid 即可，不上 drawio） |
| Pilot／客戶驗證 | Context、Container、Deployment（開始對外溝通時轉 drawio） |
| 企業級（Enterprise） | ＋Solution Overview；AI 產品加 AI Guardrails |

## 3. 圖面 metadata banner

每張圖左上（或文件引用處）必附；缺「最後校驗」的架構圖視為不可信：

```
標題｜受眾：[新人 onboarding / 跨團隊對接 / 主管與客戶簡報]
回答的問題：[一句話]
正典來源：[sad §n / ADR-*]｜最後校驗：YYYY-MM-DD
```

## 4. 全域視覺規範

### 4.1 語意化配色（drawio 內建色票）

| 語意 | 填色 fill | 框線 stroke |
|---|---|---|
| 即時／關鍵熱路徑 | `#F8CECC` 紅 | `#B85450` |
| 營運／後台面 | `#DAE8FC` 藍 | `#6C8EBF` |
| 平台共用服務 | `#D5E8D4` 綠 | `#82B366` |
| 獨立子系統 | `#B0E3E6` 青 | `#0E8088` |
| AI／能力資產 | `#FFE6CC` 橘 | `#D79B00` |
| 設計態／設定／DSL | `#FFF2CC` 黃 | `#D6B656` |
| 外部實體／actor | `#F5F5F5` 灰 | `#666666` |
| Data Store | `#E1D5E7` 紫 | `#9673A6` |

### 4.2 形狀

元件／程序＝圓角矩形；外部實體／系統＝直角矩形；人／角色＝actor；資料儲存＝圓柱；分層／部署區／子系統＝container / swimlane。

### 4.3 線型（語意化）

| 線型 | 語意 |
|---|---|
| 粗實線（strokeWidth≥2.5）、實心箭頭 | 關鍵主鏈 |
| 一般實線 | 同步呼叫／設計態發布 |
| 虛線 | 非同步／回流（事件、語料） |
| 點線、淡色 | 橫切支撐（共用服務→各區） |

未落地的目標狀態一律標 `🔜`，不得畫成與現況同權重。

## 5. 生成管線（_tools）與範例（_examples）

AI 或人**不直接手寫 drawio XML**（必疊線、必亂版面），走三步管線：

1. **宣告式 spec**：依模板 §2 的 prompt 寫一份 Python spec（擺 node、拉 edge、放 legend），引擎 [`_tools/drawio_kit.py`](./_tools/drawio_kit.py) 負責 style 與 XML。
2. **生成**：`python3 <spec>.py` → `.drawio`（可匯入 draw.io 繼續編輯；**絕不手改生成物**，重生會覆蓋）。
3. **版面驗收**：`python3 _tools/analyze_layout.py <path> -v` 量測連線交叉（cross）與穿越節點（pierce），**目標 score=0**；不合格回 spec 調座標或 waypoint 重生。

Few-shot 錨點在 [`_examples/`](./_examples/)：虛構專案 ACME Field Service 的
[填好版 prompt](./_examples/prompt_filled.md) → [spec](./_examples/acme_solution_overview.py) → `.drawio`（score=0），
含「長線走專用通道、共端點消交叉、行列擺位消長垂直線」的版面心法。

備援路徑：AI 先出 mermaid，再匯入 draw.io（Arrange → Insert → Advanced → Mermaid）手動排版——適合一次性、不需重生的圖。

## 6. style 字串庫

不經管線、直接寫 XML 或在 draw.io「Edit Style」貼用時，抄這裡（hex 依 §4.1 語意換色）：

| 用途 | style 字串（以藍為例） |
|---|---|
| 元件（圓角矩形） | `rounded=1;whiteSpace=wrap;html=1;fillColor=#DAE8FC;strokeColor=#6C8EBF;` |
| 外部系統（直角） | `whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#666666;` |
| 資料儲存（圓柱） | `shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=12;fillColor=#E1D5E7;strokeColor=#9673A6;` |
| 人／角色 | `shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fillColor=#F5F5F5;strokeColor=#666666;` |
| 分組容器 | `rounded=1;whiteSpace=wrap;html=1;fillColor=#D5E8D4;strokeColor=#82B366;verticalAlign=top;fontStyle=1;fontSize=13;container=1;collapsible=0;` |
| L1 Zone（overview） | `swimlane;html=1;whiteSpace=wrap;horizontal=1;startSize=36;fillColor=#FFFFFF;swimlaneFillColor=#F8FAFC;strokeColor=#CBD5E1;fontStyle=1;fontSize=12;container=1;collapsible=0;` |
| 註記小卡 | `rounded=1;whiteSpace=wrap;html=1;fillColor=#FFF2CC;strokeColor=#D6B656;align=left;verticalAlign=top;fontSize=11;dashed=1;` |
| 關鍵主鏈（線） | `html=1;strokeWidth=2.5;endArrow=classic;endFill=1;strokeColor=#333333;fontSize=10;` |
| 同步呼叫（線） | `html=1;endArrow=classic;endFill=1;strokeColor=#555555;fontSize=10;` |
| 非同步回流（線） | `html=1;endArrow=classic;dashed=1;strokeColor=#6C8EBF;fontSize=10;` |
| 橫切支撐（線） | `html=1;endArrow=open;dashed=1;dashPattern=1 4;strokeColor=#999999;fontSize=10;` |
| 互動路徑（overview 藍） | `edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2.5;endArrow=classic;endFill=1;strokeColor=#2563EB;fontColor=#1E3A8A;fontSize=9;` |
| 事件路徑（overview 綠） | `edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;endArrow=classic;endFill=1;dashed=1;dashPattern=6 4;strokeColor=#16A34A;fontColor=#166534;fontSize=9;` |
| 控制路徑（overview 紫） | `edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;endArrow=open;endFill=0;dashed=1;dashPattern=3 4;strokeColor=#9333EA;fontColor=#6B21A8;fontSize=9;` |
| 持久化路徑（overview 橘） | `edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;endArrow=classic;endFill=1;dashed=1;dashPattern=8 4;strokeColor=#EA580C;fontColor=#9A3412;fontSize=9;` |

完整清單（含 🔜 虛框元件卡、責任卡）見 [`_tools/drawio_kit.py`](./_tools/drawio_kit.py)——字串庫與引擎同源，改 style 只改 kit。

## 7. 通則

1. **一圖一問題一受眾**——一張圖回答不了的，拆成兩張。
2. **每張圖必附圖例**，只列該圖實際用到的配色與線型。
3. **責任清單用表格、不用圖**——元件責任目錄放 sad 表格（可 diff、可逐列追溯），卡片牆式的圖必然腐爛。
4. **程式化生成優於手拉**：批量圖以腳本從單一規格產出 `.drawio` 與 SVG／PNG，絕不手改生成物；驗收時量測連線交叉數與線穿越節點數。
5. 不同語意的資料流不得合併成同一條線（例：互動 payload 與事件 metadata 分線）。

## 8. 追溯

- 上游：[template_standard](../../_meta/template_standard.md)（模板解剖）、[workflow_manual](../../_meta/workflow_manual.md)（階段裁剪原則）
- 下游：本資料夾 5 份圖規格模板、[`_tools/`](./_tools/)（生成與驗收）、[`_examples/`](./_examples/)（few-shot 錨點）；[sad](../sad.md) §1／§5–§7 的載體選擇
