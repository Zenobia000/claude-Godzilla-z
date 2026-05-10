---
description: 根據 VibeCoding 模板進行程式碼審查，涵蓋品質、安全、架構合規。
---

# 程式碼審查

## 分析目標

分析路徑: $ARGUMENTS（預設為當前目錄）

## 審查項目

### 階段 0: 流程合規
- `3-process/workflow-manual.md` → 開發流程合規性

### 階段 1: 規劃
- `4-exploration/prd.template.md` → 需求對齊
- `3-process/bdd-guide.md` → BDD 覆蓋率

### 階段 2: 架構設計
- `1-decisions/adr.template.md` → ADR 記錄
- `1-decisions/architecture-overview.template.md` → 系統架構
- `2-contracts/api-spec.template.md` → API 設計合規

### 階段 3: 詳細設計
- `2-contracts/module-contract.template.md` → 模組規格與測試
- `5-views/project-structure.template.md` → 專案結構
- `5-views/file-dependencies.template.md` → 依賴分析
- `5-views/class-relationships.template.md` → 類別設計

### 階段 4: 開發品質
- `3-process/code-review-checklist.md` → 審查清單
- `5-views/frontend-architecture.template.md` → 前端架構
- `5-views/frontend-information-architecture.template.md` → 前端 IA

### 階段 5: 安全部署
- `3-process/security-readiness-checklist.md` → 安全評估
- `3-process/deployment-runbook.template.md` → 部署策略

### 階段 6: 維護管理
- `3-process/docs-maintenance-guide.md` → 文檔品質
- `4-exploration/wbs.template.md` → WBS 追蹤

## 建議 Agent

根據審查結果建議適合的 Agent：

```
審查結果:

建議的 Agent:
  [1] code-quality-specialist -- 程式碼品質深度分析
  [2] security-infrastructure-auditor -- 安全稽核
  [3] test-automation-engineer -- 測試覆蓋補強

請選擇 (1-3) 或 N 跳過:
```

## 使用方式

```
/review-code              # 審查整個專案
/review-code src/api/     # 審查特定路徑
```
