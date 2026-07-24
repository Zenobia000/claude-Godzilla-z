# 需求追溯駕駛艙（Excel）指南

> 可填的 `.xlsx` 範本：[`VibeCoding_Workflow_Templates/governance_workbook_template.xlsx`](../../VibeCoding_Workflow_Templates/governance_workbook_template.xlsx)

## 1. 兩個平面：看板 vs 訂版文件

開發時最耗神的是**文件切換與資訊過載**。解法是把資訊分成兩個用途不同的平面，各用各的方法：

| 平面 | 是什麼 | 工具 | 誰維護 | 填寫時機 |
|---|---|---|---|---|
| **控制/追溯（看板）** | 活的狀態與決策，掃一眼掌握全局 | 這本 Excel 駕駛艙 | 人（架構師/PM）| 滾動更新，永遠填不「完」|
| **知識/規格（訂版）** | 版本化的工程細節、建置真相源 | `docs/` Markdown、ADR、code | AI 起草、人 review | Just-in-time，功能要開發才展開 |

**鐵律：看板只放骨架（ID＋狀態＋一句話＋連結），細節不複製進看板。** 看板的一列連到它的 spec doc，不把整份 spec 塞進儲存格。

## 2. 駕駛艙的核心：一列 = 一條完整鏈

以**架構師視角**設計——一個不必親自寫每行 code 也要掌握全局的角色。每一列把一個需求橫向串起來，左到右就是語域 L1 → L2 → L3：

| 分組 | 欄位 | 誰填 |
|---|---|---|
| **業務 L1** | 需求ID、VOC/需求（業務語言）、優先序、範圍、里程碑 | PM／業務決策 |
| **橋接 L2** | FR/NFR-ID、ACPT-ID | 架構師（VOC→FR/NFR 是架構師的工作）|
| **工程 L3** | SAD元件/MOD、關鍵ADR、Code reality | 架構師／RD |
| **狀態** | 狀態、備註、文件連結 | 人滾動更新 |

掃一眼就能連結「這個需求 → 對應哪個 FR/NFR → 落在哪個 SAD 元件 → 現在什麼狀態」，不用開十個檔。

## 3. 狀態是滾動的

`狀態` 欄用下拉：`開放 / 進行中 / Pending / 結束 / Deferred`。這反映實務——需求先確定、開發功能導向、里程碑滾動調整，你不可能一開始就填滿。看板支援增量填入，`② 決策沿革` 分頁記錄每次滾動調整（誰、何時、為什麼）。

## 4. 認知負載鐵律（給 AI 的約束）

看板是**給眼睛掃的，不是給你讀的**。因此：

- AI 更新的是**結構化欄位**（駕駛艙儲存格）和對應的 **docs**，不是產出大段說明。
- AI 回報只給**短 delta**：「`DEC-003` 進 In Dev、補了 `FR-007`、連到 `sad.md#agt`」，不倒整段分析。
- 人在看板上做決策（優先序、範圍、狀態轉換、Gate）；AI 做決策之間的執行（起草 doc、寫 code、跑測試）。

## 5. 怎麼用（一人分飾多角）

```
① 需求駕駛艙（人做決策）
      │  某需求狀態轉 進行中
      ▼
② docs 訂版 + code（AI 起草、人 review）
      │  完成 → 回看板改狀態、貼連結
      ▼
   滾動下一個
```

從 `governance_workbook_template.xlsx` 複製到專案，只維護看板（狀態、決策、備註、連結）；FR/NFR、SAD、測試的細節在 `docs/` 訂版。需求決策欄位的權威定義見 [`01_requirements/requirement_decision_record.md`](../../VibeCoding_Workflow_Templates/01_requirements/requirement_decision_record.md)。
