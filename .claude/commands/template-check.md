---
description: 驗證專案是否符合指定的 VibeCoding 工作流模板規範。
---

# 模板合規檢查

## 選擇模板: $ARGUMENTS

## 可用模板

### 階段 0: 流程
1. **workflow-manual** → `3-process/workflow-manual.md`

### 階段 1: 規劃 (02-03)
2. **project-brief** → `4-exploration/prd.template.md`
3. **bdd** → `3-process/bdd-guide.md`

### 階段 2: 架構設計 (04-06)
4. **adr** → `1-decisions/adr.template.md`
5. **architecture** → `1-decisions/architecture-overview.template.md`
6. **api** → `2-contracts/api-spec.template.md`

### 階段 3: 詳細設計 (07-10)
7. **tests** → `2-contracts/module-contract.template.md`
8. **structure** → `5-views/project-structure.template.md`
9. **dependencies** → `5-views/file-dependencies.template.md`
10. **classes** → `5-views/class-relationships.template.md`

### 階段 4: 開發品質 (11-12, 17)
11. **code-review** → `3-process/code-review-checklist.md`
12. **frontend-arch** → `5-views/frontend-architecture.template.md`
13. **frontend-ia** → `5-views/frontend-information-architecture.template.md`

### 階段 5: 安全部署 (13-14)
14. **security** → `3-process/security-readiness-checklist.md`
15. **deployment** → `3-process/deployment-runbook.template.md`

### 階段 6: 維護管理 (15-16)
16. **documentation** → `3-process/docs-maintenance-guide.md`
17. **wbs** → `4-exploration/wbs.template.md`

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
