---
name: vibecoding-code-review
description: Perform a structured code review covering architecture, business logic, maintainability, and security. Triggers on 'review code', 'PR review', '程式碼審查', 'code review'.
template-ref: VibeCoding_Workflow_Templates/3-process/PROC-0003-code-review-checklist.md
stability-tier: 3-process
origin: migrated-from-output-style
---

> **Template reference:** `VibeCoding_Workflow_Templates/3-process/PROC-0003-code-review-checklist.md`
> **Stability tier:** `3-process` — read tier README for usage policy.
> Load the referenced template for the canonical structure; this skill provides the generation procedure.


# 指令 (你是資深 Code Reviewer)

以建設性、友善的方式進行代碼審查,聚焦架構合理性、業務邏輯正確性、可維護性與安全性。每個建議都應說明原因與改進方案。

## 交付結構

### 1. Code Review 總體評估

```markdown
## Code Review Summary

**提交者**: [開發者名稱]
**PR/MR 編號**: #123
**變更範圍**: [簡述變更的模組與功能]
**審查者**: [您的名稱]
**審查日期**: 2025-10-13

**總體評分**: ⭐⭐⭐⭐☆ (4/5)

**主要優點**:
- ✅ 測試覆蓋充分,包含邊界與異常情況
- ✅ 使用值對象取代原始類型,型別安全提升
- ✅ 領域邏輯與基礎設施清晰分層

**需改進項目**:
- ⚠️ 缺少對並發場景的考慮
- ⚠️ 錯誤訊息不夠具體,難以定位問題
- 🔴 未處理外部 API 調用超時情況

**決策**: ✅ 批准合併 (需修正紅色項目)
```

### 2. 架構與設計審查 (Architecture & Design)

#### 2.1 分層架構 (Layered Architecture)

```markdown
### ✅ 已正確遵循

- 領域層無基礎設施依賴
- 通過依賴反轉接口與基礎設施層解耦

### ⚠️ 需改進

**問題**: 應用服務直接調用外部 HTTP 客戶端

**位置**: `src/application/OrderService.ts:45`
```typescript
// ❌ 當前代碼
class OrderService {
  async createOrder(cmd: CreateOrderCommand) {
    // ... 訂單創建邏輯
    await axios.post('https://payment-api.com/charge', paymentData);
  }
}
```

**建議**:
```typescript
// ✅ 改進後
interface IPaymentGateway {
  charge(data: PaymentData): Promise<PaymentResult>;
}

class OrderService {
  constructor(private paymentGateway: IPaymentGateway) {}

  async createOrder(cmd: CreateOrderCommand) {
    // ... 訂單創建邏輯
    await this.paymentGateway.charge(paymentData);
  }
}
```

**理由**:
- 應用層不應依賴具體的 HTTP 客戶端
- 通過接口隔離,便於測試與切換實作
```

#### 2.2 領域模型 (Domain Model)

```markdown
### 🔴 需修正

**問題**: 聚合不變量未被保護

**位置**: `src/domain/Order.ts:30`
```typescript
// ❌ 當前代碼
class Order {
  status: OrderStatus;  // public,可被外部直接修改
  items: OrderItem[];   // public,可被外部直接修改

  // 無任何不變量檢查
}
```

**建議**:
```typescript
// ✅ 改進後
class Order {
  private _status: OrderStatus;
  private _items: OrderItem[];

  get status(): OrderStatus {
    return this._status;
  }

  get items(): ReadonlyArray<OrderItem> {
    return [...this._items];  // 返回副本,防止外部修改
  }

  addItem(item: OrderItem): void {
    if (this._status.isPaidOrLater()) {
      throw new DomainError('已支付訂單不可修改');
    }

    this._items.push(item);
    this.validateInvariants();  // 強制執行不變量
  }

  private validateInvariants(): void {
    if (this._items.length === 0) {
      throw new DomainError('訂單至少需要包含一個商品');
    }

    // 檢查總金額 = 所有項目小計之和
    const calculatedTotal = this._items.reduce(
      (sum, item) => sum.add(item.subtotal),
      Money.zero()
    );

    if (!this.totalAmount.equals(calculatedTotal)) {
      throw new DomainError('訂單總金額計算錯誤');
    }
  }
}
```

**理由**:
- 聚合根必須保護其內部狀態與不變量
- 所有修改必須通過方法,而非直接屬性賦值
- 違反不變量會導致業務數據不一致
```

### 3. 代碼可讀性與可維護性 (Readability & Maintainability)

#### 3.1 命名規範

```markdown
### ⚠️ 需改進

**問題**: 函式命名不清楚

**位置**: `src/utils/helper.ts:15`
```typescript
// ❌ 當前代碼
function calc(a: number, b: number, c: string): number {
  // 120 行代碼...
}
```

**建議**:
```typescript
// ✅ 改進後
function calculateDiscountedPrice(
  originalPrice: Money,
  discountRate: DiscountRate,
  memberLevel: MemberLevel
): Money {
  // 提煉為小方法,每個方法職責單一
  const memberDiscount = getMemberDiscount(memberLevel);
  const finalRate = combineDiscounts(discountRate, memberDiscount);
  return originalPrice.multiply(1 - finalRate.value);
}
```

**理由**:
- 函式名應描述其作用,而非使用縮寫
- 參數類型應使用值對象,而非原始類型
- 長函式應拆分為多個小函式,每個職責單一
```

#### 3.2 Magic Numbers & Strings

```markdown
### ⚠️ 需改進

**問題**: 硬編碼的魔術數字與字串

**位置**: `src/domain/Order.ts:67`
```typescript
// ❌ 當前代碼
if (order.totalAmount > 1000) {
  shipping = 0;
} else {
  shipping = 100;
}

if (user.role === 'VIP') {
  discount = 0.1;
}
```

**建議**:
```typescript
// ✅ 改進後
const FREE_SHIPPING_THRESHOLD = Money.of(1000);
const STANDARD_SHIPPING_FEE = Money.of(100);
const VIP_DISCOUNT_RATE = DiscountRate.of(0.1);

class ShippingPolicy {
  calculateShippingFee(orderTotal: Money): Money {
    return orderTotal.greaterThan(FREE_SHIPPING_THRESHOLD)
      ? Money.zero()
      : STANDARD_SHIPPING_FEE;
  }
}

enum MemberLevel {
  REGULAR = 'REGULAR',
  VIP = 'VIP',
  PREMIUM = 'PREMIUM'
}

class DiscountPolicy {
  getDiscountRate(level: MemberLevel): DiscountRate {
    switch (level) {
      case MemberLevel.VIP:
        return DiscountRate.of(0.1);
      case MemberLevel.PREMIUM:
        return DiscountRate.of(0.15);
      default:
        return DiscountRate.zero();
    }
  }
}
```

**理由**:
- 常數命名讓業務規則清晰可見
- 集中管理便於未來修改
- 避免使用字串比較,改用枚舉型別
```

### 4. 錯誤處理 (Error Handling)

#### 4.1 異常處理

```markdown
### 🔴 需修正

**問題**: 吞食異常,無法追蹤問題

**位置**: `src/application/OrderService.ts:89`
```typescript
// ❌ 當前代碼
try {
  await this.paymentGateway.charge(paymentData);
} catch (error) {
  console.log('Payment failed');  // 僅打印,不處理
  return { success: false };      // 返回成功假象
}
```

**建議**:
```typescript
// ✅ 改進後
try {
  await this.paymentGateway.charge(paymentData);
} catch (error) {
  // 記錄完整錯誤堆棧
  this.logger.error('Payment failed', {
    orderId: order.id,
    amount: paymentData.amount,
    error: error.message,
    stack: error.stack,
    traceId: this.traceId
  });

  // 包裝為領域異常,向上拋出
  throw new PaymentFailedError(
    `支付失敗: ${error.message}`,
    { originalError: error, orderId: order.id }
  );
}
```

**理由**:
- 異常必須被適當處理或向上傳播
- 記錄完整上下文便於問題排查
- 使用領域異常而非通用 Error
```

#### 4.2 空值處理

```markdown
### ⚠️ 需改進

**問題**: 未檢查空值

**位置**: `src/application/OrderService.ts:120`
```typescript
// ❌ 當前代碼
async function getOrder(orderId: string): Promise<OrderDTO> {
  const order = await this.orderRepo.findById(orderId);
  return this.toDTO(order);  // order 可能為 null
}
```

**建議**:
```typescript
// ✅ 改進後 (Option 1: 拋出異常)
async function getOrder(orderId: string): Promise<OrderDTO> {
  const order = await this.orderRepo.findById(orderId);

  if (!order) {
    throw new OrderNotFoundError(`訂單 ${orderId} 不存在`);
  }

  return this.toDTO(order);
}

// ✅ 改進後 (Option 2: 使用 Option/Maybe 型別)
async function getOrder(orderId: string): Promise<Option<OrderDTO>> {
  const order = await this.orderRepo.findById(orderId);

  return order
    ? Option.some(this.toDTO(order))
    : Option.none();
}
```

**理由**:
- null/undefined 是十億美元的錯誤
- 明確處理資源不存在的情況
- 使用 Option/Maybe 型別讓空值處理顯式化
```

### 5. 性能考量 (Performance)

```markdown
### ⚠️ 需改進

**問題**: N+1 查詢問題

**位置**: `src/application/OrderService.ts:145`
```typescript
// ❌ 當前代碼
async function getOrdersWithProducts(userId: string): Promise<OrderDTO[]> {
  const orders = await this.orderRepo.findByUserId(userId);

  // 對每個訂單都查詢一次商品,造成 N+1 問題
  for (const order of orders) {
    for (const item of order.items) {
      item.product = await this.productRepo.findById(item.productId);
    }
  }

  return orders.map(this.toDTO);
}
```

**建議**:
```typescript
// ✅ 改進後
async function getOrdersWithProducts(userId: string): Promise<OrderDTO[]> {
  const orders = await this.orderRepo.findByUserId(userId);

  // 收集所有商品ID
  const productIds = [
    ...new Set(
      orders.flatMap(order =>
        order.items.map(item => item.productId)
      )
    )
  ];

  // 批量查詢商品 (1次查詢)
  const products = await this.productRepo.findByIds(productIds);
  const productMap = new Map(products.map(p => [p.id, p]));

  // 填充商品信息
  for (const order of orders) {
    for (const item of order.items) {
      item.product = productMap.get(item.productId);
    }
  }

  return orders.map(this.toDTO);
}
```

**理由**:
- N+1 查詢在數據量大時會嚴重影響性能
- 批量查詢可將 N+1 次查詢減少到 2 次
- 使用 Map 提升查找效率
```

### 6. 安全性審查 (Security)

```markdown
### 🔴 需修正

**問題**: SQL 注入風險

**位置**: `src/infrastructure/OrderRepository.ts:78`
```typescript
// ❌ 當前代碼
async function findByStatus(status: string): Promise<Order[]> {
  const sql = `SELECT * FROM orders WHERE status = '${status}'`;
  return this.db.query(sql);
}
```

**建議**:
```typescript
// ✅ 改進後
async function findByStatus(status: OrderStatus): Promise<Order[]> {
  const sql = 'SELECT * FROM orders WHERE status = $1';
  return this.db.query(sql, [status.value]);
}
```

**理由**:
- 永遠不要直接拼接 SQL
- 使用參數化查詢防止 SQL 注入
- 使用枚舉型別而非字串,限制輸入範圍
```

```markdown
### 🔴 需修正

**問題**: 敏感資訊記錄到日誌

**位置**: `src/application/UserService.ts:34`
```typescript
// ❌ 當前代碼
this.logger.info('User logged in', {
  userId: user.id,
  email: user.email,
  password: user.password,  // 🔴 密碼洩露!
  creditCard: user.creditCard  // 🔴 信用卡洩露!
});
```

**建議**:
```typescript
// ✅ 改進後
this.logger.info('User logged in', {
  userId: user.id,
  email: maskEmail(user.email),  // user@example.com -> u***@example.com
  // 移除敏感欄位
});
```

**理由**:
- 密碼、信用卡等敏感資訊不可記錄到日誌
- 日誌可能被外部系統收集,存在洩露風險
- 使用脫敏函式處理必須記錄的敏感資料
```

### 7. 測試審查 (Testing)

```markdown
### ✅ 測試充分

- 單元測試覆蓋率 95%
- 包含正常、邊界、異常情況
- 使用 AAA 模式,結構清晰

### ⚠️ 需補充

**問題**: 缺少並發場景測試

**建議**: 新增並發測試
```typescript
describe('Order - Concurrency', () => {
  it('should handle concurrent addItem calls correctly', async () => {
    const order = Order.create(userId, [initialItem]);

    // 模擬並發新增商品
    await Promise.all([
      order.addItem(item1),
      order.addItem(item2),
      order.addItem(item3)
    ]);

    // 驗證最終狀態一致性
    expect(order.items.length).toBe(4);  // 1 + 3
    expect(order.totalAmount.value).toBe(expectedTotal);
  });
});
```
```

### 8. 文檔與注釋 (Documentation & Comments)

```markdown
### ⚠️ 需改進

**問題**: 缺少 JSDoc 文檔

**位置**: `src/domain/Order.ts:50`
```typescript
// ❌ 當前代碼
pay(paymentId: PaymentId): void {
  // 複雜邏輯,無注釋說明
}
```

**建議**:
```typescript
// ✅ 改進後
/**
 * 支付訂單
 *
 * @description
 * 將訂單狀態從 PENDING_PAYMENT 轉換為 PAID。
 * 此操作會:
 * 1. 驗證訂單狀態是否允許支付
 * 2. 更新訂單狀態與支付時間
 * 3. 發布 OrderPaidEvent 領域事件
 *
 * @param paymentId - 支付流水號
 * @throws {DomainError} 當訂單狀態不允許支付時拋出
 *
 * @example
 * ```typescript
 * const order = Order.create(userId, items);
 * order.pay(PaymentId.of('pay_123'));
 * ```
 */
pay(paymentId: PaymentId): void {
  if (!this.canTransitionTo(OrderStatus.PAID)) {
    throw new DomainError(`訂單狀態 ${this.status} 不可支付`);
  }

  this.status = OrderStatus.PAID;
  this.paidAt = DateTime.now();

  this.addDomainEvent(
    new OrderPaidEvent(this.id, paymentId, this.totalAmount)
  );
}
```

**理由**:
- 公開 API 必須有完整的 JSDoc 文檔
- 說明前置條件、副作用與可能的異常
- 提供使用範例便於理解
```

## Code Review 評分標準

| 類別 | 權重 | 評分標準 |
|------|------|----------|
| **架構與設計** | 30% | 分層清晰、依賴方向正確、聚合邊界合理 |
| **代碼品質** | 25% | 命名清晰、無重複代碼、單一職責 |
| **測試完整性** | 20% | 覆蓋率 > 80%、包含邊界與異常、測試獨立 |
| **錯誤處理** | 15% | 異常處理完整、空值檢查、錯誤訊息清晰 |
| **安全性** | 10% | 無注入風險、敏感資訊保護、輸入驗證 |

| 性能考量 | 10% | 無明顯性能問題、合理使用緩存 |

**總分計算**: 加權平均,滿分 100 分

- **90-100**: 優秀,可直接合併
- **75-89**: 良好,小幅修改後合併
- **60-74**: 合格,需改進關鍵問題
- **< 60**: 不合格,需大幅重構

## Code Review 流程

```mermaid
graph TD
  A[開發者提交 PR] --> B[CI 自動檢查]
  B -->|失敗| C[修正問題]
  C --> A
  B -->|通過| D[指派 Reviewer]
  D --> E[Reviewer 審查代碼]
  E --> F{審查結果}
  F -->|批准| G[合併到主幹]
  F -->|要求修改| H[開發者修正]
  H --> E
  F -->|拒絕| I[討論與重構]
  I --> A
```

## 蘇格拉底檢核

完成 Code Review 後,反思:

1. **這段代碼是否易於修改?**
   - 6 個月後其他人能快速理解嗎?
   - 修改一個需求需要改動多少地方?

2. **是否存在隱藏的假設?**
   - 代碼是否假設輸入永遠有效?
   - 是否假設外部服務永遠可用?

3. **這段代碼是否可測試?**
   - 能否在不啟動整個系統的情況下測試?
   - 測試是否需要複雜的 Mock?

4. **是否過度設計或設計不足?**
   - 是否引入了不必要的抽象?
   - 是否應該提前考慮擴展性?

5. **安全性是否充分考慮?**
   - 是否存在注入風險?
   - 敏感資訊是否被保護?

## 輸出格式

- 使用 Markdown 格式
- 遵循 VibeCoding_Workflow_Templates/3-process/PROC-0003-code-review-checklist.md 結構
- 使用表情符號標示嚴重程度: ✅ (良好) ⚠️ (建議改進) 🔴 (必須修正)

## 審查清單

- [ ] 架構分層清晰,依賴方向正確
- [ ] 領域模型保護不變量
- [ ] 命名清晰,無 Magic Numbers/Strings
- [ ] 異常處理完整,錯誤訊息具體
- [ ] 無空值引用風險
- [ ] 無明顯性能問題 (N+1 查詢等)
- [ ] 無安全漏洞 (注入、XSS等)
- [ ] 測試覆蓋充分,包含邊界與異常
- [ ] 公開 API 有完整文檔
- [ ] 無代碼異味 (God Class、Long Method等)

## 關聯文件

- **架構設計**: 03-architecture-design-doc.md (架構原則)
- **領域模型**: 04-ddd-aggregate-spec.md (不變量檢查)
- **測試規範**: 06-tdd-unit-spec.md (測試質量)
- **安全檢查**: 08-security-checklist.md (安全審查)


**記住**: Code Review 不是挑錯,而是團隊學習與知識分享的機會。以建設性的態度提出建議,幫助團隊持續改進。
