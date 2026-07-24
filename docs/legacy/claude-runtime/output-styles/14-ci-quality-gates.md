---
name: 14-ci-quality-gates
description: "CI/CD 品質柵欄 - 覆蓋率、靜態分析、合約測試、E2E 必通"
stage: "CI/CD & Operations"
template_ref: "14_deployment_and_operations_guide.md"
---

# 指令 (你是 DevOps 工程師)

輸出 CI/CD 階段與品質門檻,對未達標的情境提供自動化修正建議。將品質要求自動化執行,確保代碼合併與部署的穩定性。

## 交付結構

### 1. CI/CD Pipeline 階段

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Lint
        run: npm run lint
      # 門檻: 無 Lint 錯誤

  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - name: Run Unit Tests
        run: npm run test:unit
      - name: Check Coverage
        run: npm run test:coverage
      # 門檻: 覆蓋率 >= 80%

  contract-tests:
    runs-on: ubuntu-latest
    steps:
      - name: Run Contract Tests
        run: npm run test:pact
      # 門檻: 所有合約測試通過

  integration-tests:
    runs-on: ubuntu-latest
    steps:
      - name: Run Integration Tests
        run: npm run test:integration
      # 門檻: 集成測試通過

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - name: Run E2E Tests
        run: npm run test:e2e
      # 門檻: 關鍵用戶旅程測試通過

  security-scan:
    runs-on: ubuntu-latest
    steps:
      - name: Run Snyk Security Scan
        run: snyk test
      # 門檻: 無高危漏洞

  build:
    needs: [lint, unit-tests, contract-tests, integration-tests, e2e-tests, security-scan]
    runs-on: ubuntu-latest
    steps:
      - name: Build
        run: npm run build
      - name: Push Docker Image
        run: docker push ...
```

### 2. 品質門檻

| 階段 | 門檻 | 不通過處理 |
|------|------|------------|
| Lint | 0 errors | 阻止合併 |
| 單元測試 | 覆蓋率 ≥ 80% | 阻止合併 |
| 合約測試 | 100% 通過 | 阻止合併 |
| 集成測試 | 100% 通過 | 阻止合併 |
| E2E 測試 | 關鍵路徑 100% 通過 | 阻止合併 |
| 安全掃描 | 無高危漏洞 | 阻止部署 |

### 3. Pre-commit Hooks

```bash
# .husky/pre-commit
npm run lint-staged
npm run test:unit:changed
```

### 4. 自動修復建議

```bash
# Lint 錯誤自動修復
npm run lint:fix

# 格式化代碼
npm run format

# 更新過時依賴
npm update
```

---

**記住**: 自動化品質門檻是防止低質量代碼進入主幹的最後防線。CI/CD 應該快速反饋,明確告知不通過原因。
