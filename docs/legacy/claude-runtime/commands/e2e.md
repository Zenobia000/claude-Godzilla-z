---
description: 使用 Playwright 生成並執行端到端測試。建立測試旅程、執行測試、擷取截圖/影片/trace。
---

# E2E 指令

此指令呼叫 **e2e-validation-specialist** agent 來生成、維護和執行 Playwright 端到端測試。

## 功能說明

1. **生成測試旅程** - 為使用者流程建立 Playwright 測試
2. **執行 E2E 測試** - 跨瀏覽器執行測試
3. **擷取成品** - 失敗時的截圖、影片、trace
4. **上傳結果** - HTML 報告和 JUnit XML
5. **識別不穩定測試** - 隔離不穩定的測試

## 使用時機

- 測試關鍵使用者旅程（登入、核心流程、支付）
- 驗證多步驟流程端到端運作
- 測試 UI 互動和導覽
- 驗證前後端整合
- 準備生產部署

## 運作方式

e2e-validation-specialist agent 會：

1. **分析使用者流程**並識別測試場景
2. **生成 Playwright 測試**使用 Page Object Model 模式
3. **跨多瀏覽器執行測試**（Chrome、Firefox、Safari）
4. **擷取失敗**的截圖、影片和 trace
5. **生成報告**含結果和成品
6. **識別不穩定測試**並建議修復

## 快速指令

```bash
# 執行所有 E2E 測試
npx playwright test

# 執行特定測試檔案
npx playwright test tests/e2e/auth.spec.ts

# 顯示瀏覽器模式
npx playwright test --headed

# 除錯模式
npx playwright test --debug

# 生成測試程式碼
npx playwright codegen http://localhost:3000

# 檢視報告
npx playwright show-report
```

## 最佳實踐

**應該做:**
- 使用 Page Object Model 提高可維護性
- 使用 data-testid 屬性定位元素
- 等待 API 回應而非任意超時
- 測試關鍵使用者旅程端到端
- 合併前執行測試
- 失敗時檢視成品

**不應該做:**
- 使用脆弱的選擇器（CSS class 會變更）
- 測試實作細節
- 對生產環境執行測試
- 忽略不穩定測試
- 用 E2E 測試每個邊界情況（使用單元測試）

## 與其他指令的搭配

- 用 `/plan` 識別要測試的關鍵旅程
- 用 `/tdd` 做單元測試（更快、更細粒度）
- 用 `/e2e` 做整合和使用者旅程測試
- 用 `/review-code` 驗證測試品質
