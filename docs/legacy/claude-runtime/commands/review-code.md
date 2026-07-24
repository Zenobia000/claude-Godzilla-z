---
description: 根據 VibeCoding 模板進行程式碼審查，涵蓋品質、安全、架構合規。
---

# 程式碼審查

## 分析目標

分析路徑: $ARGUMENTS（預設為當前目錄）

## 審查項目

### 階段 0: 流程合規
- `01_workflow_manual.md` → 開發流程合規性

### 階段 1: 規劃
- `02_project_brief_and_prd.md` → 需求對齊
- `03_behavior_driven_development_guide.md` → BDD 覆蓋率

### 階段 2: 架構設計
- `04_architecture_decision_record_template.md` → ADR 記錄
- `05_architecture_and_design_document.md` → 系統架構
- `06_api_design_specification.md` → API 設計合規

### 階段 3: 詳細設計
- `07_module_specification_and_tests.md` → 模組規格與測試
- `08_project_structure_guide.md` → 專案結構
- `09_file_dependencies_template.md` → 依賴分析
- `10_class_relationships_template.md` → 類別設計

### 階段 4: 開發品質
- `11_code_review_and_refactoring_guide.md` → 審查清單
- `12_frontend_architecture_specification.md` → 前端架構
- `17_frontend_information_architecture_template.md` → 前端 IA

### 階段 5: 安全部署
- `13_security_and_readiness_checklists.md` → 安全評估
- `14_deployment_and_operations_guide.md` → 部署策略

### 階段 6: 維護管理
- `15_documentation_and_maintenance_guide.md` → 文檔品質
- `16_wbs_development_plan_template.md` → WBS 追蹤

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
