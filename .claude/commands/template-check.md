---
description: 驗證專案是否符合指定的 VibeCoding 工作流模板規範。
---

# 模板合規檢查

## 選擇模板: $ARGUMENTS

## 可用模板

### 階段 0: 流程
1. **workflow-manual** → `3-process/PROC-0001-workflow-manual.md`

### 階段 1: 規劃 (02-03)
2. **project-brief** → `4-exploration/PRD-0000-prd.template.md`
3. **bdd** → `3-process/PROC-0002-bdd-guide.md`

### 階段 2: 架構設計 (04-06)
4. **adr** → `1-decisions/ADR-0000-adr.template.md`
5. **architecture** → `1-decisions/ARCH-0000-architecture-overview.template.md`
6. **api** → `2-contracts/API-0000-api-spec.template.md`

### 階段 3: 詳細設計 (07-10)
7. **tests** → `2-contracts/MC-0000-module-contract.template.md`
8. **structure** → `5-views/VIEW-0001-project-structure.template.md`
9. **dependencies** → `5-views/VIEW-0002-file-dependencies.template.md`
10. **classes** → `5-views/VIEW-0003-class-relationships.template.md`

### 階段 4: 開發品質 (11-12, 17)
11. **code-review** → `3-process/PROC-0003-code-review-checklist.md`
12. **frontend-design** → `2-contracts/DS-0000-frontend-design-system.template.md`
13. **page-contract** → `2-contracts/PC-0000-page-contract.template.md`

### 階段 5: 安全部署 (13-14)
14. **security** → `3-process/PROC-0004-security-readiness-checklist.md`
15. **deployment** → `3-process/PROC-0005-deployment-runbook.template.md`

### 階段 6: 維護管理 (15-16)
16. **documentation** → `3-process/PROC-0006-docs-maintenance-guide.md`
17. **wbs** → `4-exploration/WBS-0000-wbs.template.md`

## 合規分析

針對選定的模板檢查專案合規性：

```
模板: $ARGUMENTS
合規分析:

  符合: [項目列表]
  需改善: [項目列表]
  缺失: [項目列表]

  整體合規: [X]%

建議:
  [Y] 啟動對應 Agent 改善
  [R] 產生詳細報告
  [C] 交叉檢查其他模板
  [N] 稍後處理
```

## 使用方式

```
/template-check security       # 檢查安全合規
/template-check architecture   # 檢查架構合規
/template-check api            # 檢查 API 合規
```
