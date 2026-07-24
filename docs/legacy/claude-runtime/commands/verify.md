---
description: 對當前程式碼庫狀態執行全面驗證檢查。
---

# 驗證指令

## 說明

依以下確切順序執行驗證：

### 1. 建置檢查
- 執行專案的建置指令
- 如失敗則報告錯誤並停止

### 2. 型別檢查
- 執行 TypeScript/型別檢查器
- 報告所有錯誤含檔案:行號

### 3. Lint 檢查
- 執行 linter
- 報告警告和錯誤

### 4. 測試套件
- 執行所有測試
- 報告通過/失敗數量
- 報告覆蓋率百分比

### 5. Console.log 稽核
- 搜尋原始碼中的 console.log
- 報告位置

### 6. Git 狀態
- 顯示未提交的變更
- 顯示自上次 commit 以來修改的檔案

## 輸出

產出簡潔的驗證報告：

```
VERIFICATION: [PASS/FAIL]

Build:    [OK/FAIL]
Types:    [OK/X errors]
Lint:     [OK/X issues]
Tests:    [X/Y passed, Z% coverage]
Secrets:  [OK/X found]
Logs:     [OK/X console.logs]

Ready for PR: [YES/NO]
```

如有任何關鍵問題，列出並附修復建議。

## 參數

$ARGUMENTS 可以是：
- `quick` - 僅建置 + 型別
- `full` - 所有檢查（預設）
- `pre-commit` - 與 commit 相關的檢查
- `pre-pr` - 完整檢查加安全掃描
