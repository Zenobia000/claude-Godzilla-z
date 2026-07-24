---
description: 全面品質評估，根據 VibeCoding 模板進行分析並建議適合的 Agent。
---

# 品質評估

## 分析內容

針對當前專案或指定路徑執行品質檢查：

1. **程式碼品質** -- 可讀性、複雜度、重複、命名
2. **架構合規** -- 分層結構、依賴方向、模組化
3. **測試覆蓋** -- 單元/整合/E2E 覆蓋率
4. **安全檢查** -- 硬編碼秘密、輸入驗證、注入風險
5. **模板合規** -- 對照 VibeCoding 模板檢查點

## 輸出格式

```
品質評估結果:
  程式碼品質:  [A/B/C/D]
  架構合規:    [通過/需改善]
  測試覆蓋:    [X]%
  安全檢查:    [通過/有風險]
  模板合規:    [X]%

建議的 Agent:
  [1] code-quality-specialist -- 深度程式碼審查
  [2] security-infrastructure-auditor -- 安全稽核
  [3] test-automation-engineer -- 測試補強
  [4] deployment-expert -- 部署就緒檢查

請選擇 (1-4) 或輸入 N 跳過:
```

## 使用方式

```
/check-quality              # 檢查整個專案
/check-quality src/api/     # 檢查特定目錄
```
