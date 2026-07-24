---
description: 查看專案 WBS 任務狀態總覽，追蹤進度和阻塞項。
---

# 專案狀態

## 功能

顯示 WBS 任務清單的完整狀態，包含進度、阻塞項和下一步建議。

## 資料來源

**必須** 從 `.claude/taskmaster-data/wbs.md` 讀取 WBS 資料。

如果檔案不存在，提示使用者先執行 `/task-init` 初始化專案。

## 流程

1. 讀取 `.claude/taskmaster-data/wbs.md`
2. 解析任務清單表格，統計各狀態數量
3. 顯示統計和任務清單
4. 如有任務狀態變更，**立即更新** wbs.md 檔案

## 輸出格式

```
專案狀態:
  總任務: [N] 個
  待處理: [X] 個
  進行中: [X] 個
  已完成: [X] 個
  阻塞:   [X] 個
  進度:   [=====-----] X%

VibeCoding 模板合規:
  05_architecture_and_design_document.md    [通過]
  07_module_specification_and_tests.md      [待檢查]
  08_project_structure_guide.md             [通過]
  13_security_and_readiness_checklists.md   [待檢查]

任務清單:
  [完成] 1.1 專案初始化
  [完成] 1.2 需求分析
  [進行] 2.1 架構設計           ← 當前
  [待處理] 2.2 API 設計
  [待處理] 3.1 核心功能開發
  ...

下一步建議: /task-next
```

## 更新任務狀態

當使用者告知某任務已完成或有進展時：
1. 讀取 `.claude/taskmaster-data/wbs.md`
2. 更新對應任務的狀態欄位
3. 更新「最後更新」日期
4. 寫回檔案

## 時間追蹤整合

顯示狀態時，如果 `.claude/taskmaster-data/timelog.jsonl` 存在，額外顯示：

1. 在任務清單中，對有時間記錄的任務顯示「實際時間」欄位
2. 與 WBS 預估時間對比，顯示差異
3. 顯示當前正在追蹤的任務（讀取 `.current-task`）

輸出範例：
```
任務清單:
  [完成] 1.1 專案初始化          預估 0.5h │ 實際 0h25m ✅
  [完成] 1.2 需求分析            預估 2h   │ 實際 1h50m ✅
  [進行] 2.1 架構設計     ⏱️     預估 2h   │ 已花 1h15m（進行中）
  [待處理] 2.2 API 設計          預估 1h   │ --
```

## 使用方式

```
/task-status              # 簡要狀態
/task-status --detailed   # 含每個任務詳情
/task-status --metrics    # 含效能指標和時間追蹤
```
