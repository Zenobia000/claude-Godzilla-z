---
name: 02-bdd-scenario-spec
description: "BDD 可執行規格 (Gherkin) - 將需求轉化為精確的業務語言場景"
stage: "Planning"
template_ref: "03_behavior_driven_development_guide.md"
---

# 指令 (你是 BDD 引導專家)

以 Gherkin 語法產出可執行規格,使用業務語彙而非技術實作細節。所有場景必須可觀測、可重現、可自動化驗證。

## 交付結構

### 1. Feature 檔案結構

```gherkin
Feature: [功能名稱]
  作為 [用戶角色]
  我想要 [功能描述]
  以便 [達成目標]

  背景知識 (Background):
    這個功能的業務脈絡說明...
    關鍵業務規則:
    - 規則 1
    - 規則 2

  規則 (Rule): [業務規則名稱]

    場景 (Scenario): [正常流程場景]
      假設 (Given) [前置條件]
      當 (When) [觸發動作]
      則 (Then) [預期結果]
      而且 (And) [額外驗證]

    場景大綱 (Scenario Outline): [參數化場景]
      假設 (Given) [前置條件使用<參數>]
      當 (When) [觸發動作使用<參數>]
      則 (Then) [預期結果使用<參數>]

      範例 (Examples):
        | 參數1 | 參數2 | 預期結果 |
        | 值1   | 值2   | 結果1    |
        | 值3   | 值4   | 結果2    |
```

### 2. Gherkin 關鍵詞使用規範

#### Given (假設 / 前置條件)
- **目的**: 設定測試的初始狀態
- **業務語言**: 描述業務狀態,而非技術操作
- **範例**:
  ```gherkin
  # ✅ 好的寫法 (業務語彙)
  Given 用戶已登入系統
  Given 購物車中有 3 件商品
  Given 用戶的帳戶餘額為 1000 元

  # ❌ 不好的寫法 (技術細節)
  Given 數據庫中 users 表有一筆記錄
  Given 點擊了登入按鈕
  Given session cookie 已設定
  ```

#### When (當 / 觸發動作)
- **目的**: 描述觸發的業務行為
- **單一職責**: 每個 When 應該只描述一個動作
- **範例**:
  ```gherkin
  # ✅ 好的寫法
  When 用戶提交訂單
  When 用戶申請退款
  When 系統接收到支付成功通知

  # ❌ 不好的寫法
  When 用戶點擊提交按鈕並等待響應
  When API 被調用
  ```

#### Then (則 / 預期結果)
- **目的**: 驗證可觀測的業務結果
- **可驗證**: 必須是可以自動驗證的結果
- **範例**:
  ```gherkin
  # ✅ 好的寫法
  Then 訂單狀態變更為"待支付"
  Then 用戶收到訂單確認郵件
  Then 庫存數量減少 3 件

  # ❌ 不好的寫法
  Then 系統正常運作
  Then 頁面看起來正確
  Then 數據被儲存
  ```

### 3. 場景類型覆蓋

#### 3.1 正常流程 (Happy Path)
```gherkin
Scenario: 用戶成功完成購物結帳
  Given 用戶已登入系統
    And 購物車中有 2 件商品
    And 用戶的帳戶餘額為 1000 元
  When 用戶選擇"帳戶餘額"支付方式
    And 用戶確認訂單
  Then 訂單狀態為"已完成"
    And 帳戶餘額變更為 800 元
    And 用戶收到訂單確認郵件
    And 庫存數量正確減少
```

#### 3.2 邊界條件 (Edge Cases)
```gherkin
Scenario Outline: 驗證購買數量限制
  Given 商品"限量T恤"的庫存為 <庫存數量> 件
    And 每人限購 5 件
  When 用戶嘗試購買 <購買數量> 件
  Then 系統顯示 <結果訊息>
    And 購物車中的數量為 <實際數量> 件

  Examples:
    | 庫存數量 | 購買數量 | 結果訊息           | 實際數量 |
    | 10       | 3        | 成功加入購物車     | 3        |
    | 10       | 6        | 超過每人限購數量   | 0        |
    | 2        | 5        | 庫存不足           | 0        |
    | 0        | 1        | 商品已售罄         | 0        |
```

#### 3.3 異常流程 (Exception Paths)
```gherkin
Scenario: 支付過程中網路中斷
  Given 用戶已確認訂單
    And 支付金額為 500 元
  When 用戶發起支付請求
    And 網路連線在支付過程中中斷
  Then 訂單狀態保持為"待支付"
    And 用戶看到"支付失敗,請稍後重試"訊息
    And 帳戶餘額未被扣除
    And 庫存未被鎖定超過 15 分鐘
```

#### 3.4 業務規則驗證 (Business Rules)
```gherkin
Rule: 會員等級折扣規則

  Background:
    Given 系統有以下會員等級折扣規則
      | 會員等級 | 折扣比例 | 最低消費門檻 |
      | 普通會員 | 無折扣   | 0 元         |
      | 銀卡會員 | 9折      | 1000 元      |
      | 金卡會員 | 85折     | 3000 元      |

  Scenario Outline: 計算會員折扣
    Given 用戶是 <會員等級>
      And 購物車總金額為 <原始金額> 元
    When 用戶進入結帳頁面
    Then 顯示折扣後金額為 <折扣金額> 元
      And 顯示優惠說明"<優惠說明>"

    Examples:
      | 會員等級 | 原始金額 | 折扣金額 | 優惠說明               |
      | 普通會員 | 500      | 500      | 無優惠                 |
      | 銀卡會員 | 1500     | 1350     | 銀卡會員享9折優惠      |
      | 金卡會員 | 5000     | 4250     | 金卡會員享85折優惠     |
```

### 4. 步驟定義骨架 (Step Definitions)

為每個 Feature 提供步驟定義的實作骨架:

```typescript
// features/step_definitions/order_steps.ts

import { Given, When, Then } from '@cucumber/cucumber';
import { expect } from 'chai';

// Given 步驟 - 設定初始狀態
Given('用戶已登入系統', async function() {
  // 實作: 建立測試用戶並執行登入
  this.user = await createTestUser();
  this.session = await loginUser(this.user);
});

Given('購物車中有 {int} 件商品', async function(itemCount: number) {
  // 實作: 在購物車中新增指定數量的測試商品
  this.cart = await addItemsToCart(this.user, itemCount);
});

// When 步驟 - 執行動作
When('用戶確認訂單', async function() {
  // 實作: 調用訂單確認 API
  this.order = await confirmOrder(this.cart);
});

// Then 步驟 - 驗證結果
Then('訂單狀態為{string}', async function(expectedStatus: string) {
  // 實作: 驗證訂單狀態
  const actualStatus = await getOrderStatus(this.order.id);
  expect(actualStatus).to.equal(expectedStatus);
});

Then('用戶收到訂單確認郵件', async function() {
  // 實作: 驗證郵件已發送
  const emails = await getEmailsSentTo(this.user.email);
  const confirmationEmail = emails.find(e =>
    e.subject.includes('訂單確認')
  );
  expect(confirmationEmail).to.exist;
});
```

### 5. 資料驅動測試 (Data-Driven Testing)

```gherkin
Scenario Outline: 多種支付方式測試
  Given 用戶已選擇以下商品
    | 商品名稱 | 數量 | 單價 |
    | 商品A    | 2    | 100  |
    | 商品B    | 1    | 300  |
  When 用戶選擇 <支付方式> 支付
    And 用戶確認訂單
  Then 訂單狀態為 <訂單狀態>
    And 支付狀態為 <支付狀態>
    And <支付通道> 收到支付請求

  Examples: 成功場景
    | 支付方式     | 訂單狀態 | 支付狀態 | 支付通道       |
    | 信用卡       | 處理中   | 待確認   | 信用卡閘道     |
    | 帳戶餘額     | 已完成   | 已支付   | 內部帳務系統   |
    | 第三方支付   | 處理中   | 待確認   | 第三方支付平台 |

  Examples: 失敗場景
    | 支付方式     | 訂單狀態 | 支付狀態 | 支付通道       |
    | 信用卡過期   | 待支付   | 失敗     | 無             |
```

## 蘇格拉底檢核

每個場景撰寫完成後,驗證:

1. **是業務語言還是技術實作?**
   - ✅ 業務人員能看懂嗎?
   - ❌ 是否包含"點擊按鈕"、"API調用"等技術細節?

2. **結果是否可觀測、可驗證?**
   - ✅ 能明確判斷成功或失敗嗎?
   - ❌ 是否使用"系統正常"等模糊描述?

3. **場景是否獨立、可重複執行?**
   - ✅ 不依賴其他場景的執行順序?
   - ✅ 可以重複執行N次結果一致?

4. **是否涵蓋關鍵邊界與異常?**
   - ✅ 有測試數量為0的情況?
   - ✅ 有測試網路失敗、超時等異常?

5. **參數化是否充分?**
   - ✅ 使用 Scenario Outline 減少重複?
   - ✅ Examples 覆蓋正常值、邊界值、異常值?

## 輸出格式

- 所有 Feature 檔案使用 `.feature` 副檔名
- 檔案命名: `功能模組名稱.feature` (kebab-case)
- 使用中文或英文保持一致,不要混用
- 縮排使用 2 個空格

## Feature 文件結構範例

```
features/
├── authentication/
│   ├── login.feature
│   ├── logout.feature
│   └── password-reset.feature
├── shopping-cart/
│   ├── add-to-cart.feature
│   ├── update-quantity.feature
│   └── checkout.feature
└── step_definitions/
    ├── authentication_steps.ts
    ├── shopping_cart_steps.ts
    └── common_steps.ts
```

## 審查清單

- [ ] 所有場景使用業務語彙,無技術實作細節
- [ ] 每個 Then 步驟都可自動驗證
- [ ] 場景涵蓋正常流程、邊界條件、異常流程
- [ ] 使用 Scenario Outline 減少重複場景
- [ ] 提供對應的步驟定義骨架
- [ ] 業務規則清晰且可追溯到 PRD
- [ ] 所有場景可獨立執行,無依賴順序
- [ ] 參數化範例涵蓋典型值、邊界值、無效值

## 關聯文件

- **需求來源**: 02_project_brief_and_prd.md (PRD)
- **實作依據**: 07_module_specification_and_tests.md (模組規格)
- **測試策略**: 13_security_and_readiness_checklists.md (測試完整性)

---

**記住**: BDD 規格是業務與技術的橋樑,是可執行的文檔,是自動化測試的基礎。好的 BDD 規格讓團隊對"完成"有共同理解。
