---
description: 協調 Agent 委派執行任務，分析任務特性並建議最適合的 Agent。
---

# Agent 委派

## 功能

分析任務需求，建議最適合的專業 Agent，經你確認後委派執行。

## 流程

1. **任務分析** -- 解析任務複雜度、所需技能、風險等級
2. **Agent 匹配** -- 從 13 個 Agent 中選擇最適合的
3. **人類確認** -- 呈現建議，等待你的決定
4. **執行追蹤** -- Agent 執行完畢後回報結果

## 輸出格式

```
任務分析:
  任務: [任務描述]
  複雜度: [高/中/低]
  需求技能: [列表]

Agent 建議:
  最佳: [agent-name] (適合度 95%)
  替代: [agent-name] (適合度 80%)

請選擇:
  [1] 啟動建議的 Agent
  [2] 選擇替代 Agent
  [3] 指定其他 Agent
  [N] 取消
```

## 使用方式

```
/hub-delegate                           # 自動分析當前任務
/hub-delegate security                  # 指定安全稽核
/hub-delegate --task="實作登入 API"     # 指定任務描述
```

## 可用 Agent

| Agent | 專長 |
| :--- | :--- |
| planner | 功能規劃（opus） |
| architect | 架構設計（opus） |
| code-quality-specialist | 程式碼審查 |
| security-infrastructure-auditor | 安全稽核 |
| test-automation-engineer | 測試自動化 |
| tdd-guide | TDD 引導 |
| e2e-validation-specialist | E2E 測試 |
| build-error-resolver | 建置修復 |
| refactor-cleaner | 死碼清理 |
| documentation-specialist | 文檔生成 |
| deployment-expert | 部署運維 |
| workflow-template-manager | 模板管理 |
| general-purpose | 通用任務 |
