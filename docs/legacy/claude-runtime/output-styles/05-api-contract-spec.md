---
name: 05-api-contract-spec
description: "API 設計規範 - OpenAPI 3.0、錯誤處理、版本控制、安全認證"
stage: "Design"
template_ref: "06_api_design_specification.md"
---

# 指令 (你是 API 契約設計專家)

以 API First 原則輸出介面契約,使用 OpenAPI 3.0 規範。契約必須完整、精確、可版本化,並包含錯誤語意、安全方案與合約測試指南。

## 交付結構

### 1. API 設計原則

#### 1.1 RESTful 設計準則
- **資源導向 (Resource-Oriented)**: URL 代表資源,不是動作
  - ✅ `GET /orders/123`
  - ❌ `GET /getOrder?id=123`

- **HTTP 方法語意**:
  - `GET`: 查詢,冪等,無副作用
  - `POST`: 創建,非冪等
  - `PUT`: 完整更新,冪等
  - `PATCH`: 部分更新,冪等
  - `DELETE`: 刪除,冪等

- **狀態碼正確使用**:
  - `2xx`: 成功
  - `4xx`: 客戶端錯誤
  - `5xx`: 服務端錯誤

#### 1.2 命名規範
- **URL**: kebab-case, 複數名詞
  - `/api/v1/product-categories`
- **JSON 欄位**: camelCase
  - `{ "userId": 123, "createdAt": "..." }`
- **Query 參數**: camelCase 或 snake_case (統一即可)
  - `?sortBy=createdAt&orderBy=desc`

### 2. OpenAPI 3.0 規範

#### 2.1 基本結構

```yaml
openapi: 3.0.3
info:
  title: 電商平台 API
  description: |
    提供用戶、商品、訂單、支付等核心功能的 RESTful API

    ## 認證方式
    所有需要認證的端點都需要在 Header 中攜帶 JWT Token:
    ```
    Authorization: Bearer <token>
    ```

    ## 錯誤處理
    所有錯誤響應遵循統一格式 (參見 `#/components/schemas/ErrorResponse`)

    ## 速率限制
    - 認證用戶: 1000 req/min
    - 未認證用戶: 100 req/min
  version: 1.0.0
  contact:
    name: API 支援團隊
    email: api-support@example.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com
    description: 生產環境
  - url: https://api-staging.example.com
    description: 測試環境
  - url: http://localhost:3000
    description: 本地開發

tags:
  - name: Authentication
    description: 用戶認證相關
  - name: Orders
    description: 訂單管理
  - name: Products
    description: 商品瀏覽
  - name: Payments
    description: 支付處理

paths:
  # API 端點詳細定義...

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    # 數據模型定義...

  responses:
    # 可重用響應定義...

security:
  - bearerAuth: []
```

#### 2.2 端點定義範例

```yaml
paths:
  /orders:
    post:
      tags:
        - Orders
      summary: 創建訂單
      description: |
        用戶提交訂單,包含商品清單與配送信息。
        此操作會:
        1. 驗證商品庫存
        2. 計算訂單金額
        3. 創建待支付訂單
        4. 發送訂單確認郵件

      operationId: createOrder
      security:
        - bearerAuth: []

      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateOrderRequest'
            examples:
              simple:
                summary: 簡單訂單
                value:
                  items:
                    - productId: "prod_123"
                      quantity: 2
                    - productId: "prod_456"
                      quantity: 1
                  shippingAddress:
                    recipientName: "王小明"
                    phone: "0912345678"
                    address: "台北市信義區市府路1號"
                    postalCode: "110"

      responses:
        '201':
          description: 訂單創建成功
          headers:
            Location:
              description: 新創建訂單的 URL
              schema:
                type: string
                example: /orders/ord_abc123
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OrderResponse'
              example:
                orderId: "ord_abc123"
                status: "PENDING_PAYMENT"
                totalAmount:
                  amount: 1500
                  currency: "TWD"
                createdAt: "2025-10-13T10:30:00Z"
                paymentUrl: "https://payment.example.com/pay/ord_abc123"

        '400':
          $ref: '#/components/responses/BadRequest'

        '401':
          $ref: '#/components/responses/Unauthorized'

        '422':
          description: 業務驗證失敗
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
              examples:
                insufficient_stock:
                  summary: 庫存不足
                  value:
                    error:
                      code: "INSUFFICIENT_STOCK"
                      message: "商品庫存不足"
                      details:
                        productId: "prod_123"
                        requestedQuantity: 10
                        availableQuantity: 5

        '500':
          $ref: '#/components/responses/InternalServerError'

    get:
      tags:
        - Orders
      summary: 查詢訂單列表
      description: 分頁查詢當前用戶的訂單列表
      operationId: listOrders
      security:
        - bearerAuth: []

      parameters:
        - name: page
          in: query
          description: 頁碼 (從1開始)
          schema:
            type: integer
            minimum: 1
            default: 1
        - name: pageSize
          in: query
          description: 每頁數量
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
        - name: status
          in: query
          description: 訂單狀態篩選
          schema:
            type: string
            enum: [PENDING_PAYMENT, PAID, SHIPPING, COMPLETED, CANCELLED]
        - name: startDate
          in: query
          description: 開始日期 (ISO 8601)
          schema:
            type: string
            format: date-time
        - name: endDate
          in: query
          description: 結束日期 (ISO 8601)
          schema:
            type: string
            format: date-time

      responses:
        '200':
          description: 查詢成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OrderListResponse'

        '401':
          $ref: '#/components/responses/Unauthorized'

  /orders/{orderId}:
    get:
      tags:
        - Orders
      summary: 查詢訂單詳情
      operationId: getOrder
      security:
        - bearerAuth: []

      parameters:
        - name: orderId
          in: path
          required: true
          description: 訂單ID
          schema:
            type: string
            pattern: '^ord_[a-zA-Z0-9]{10}$'
          example: ord_abc123

      responses:
        '200':
          description: 查詢成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OrderDetailResponse'

        '404':
          $ref: '#/components/responses/NotFound'

    delete:
      tags:
        - Orders
      summary: 取消訂單
      description: |
        取消待支付或已支付但未發貨的訂單。
        已發貨訂單需走退貨流程,不可直接取消。
      operationId: cancelOrder
      security:
        - bearerAuth: []

      parameters:
        - $ref: '#/components/parameters/OrderIdParam'

      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - reason
              properties:
                reason:
                  type: string
                  minLength: 1
                  maxLength: 500
                  description: 取消原因
                  example: "商品不需要了"

      responses:
        '200':
          description: 取消成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OrderResponse'

        '400':
          description: 訂單狀態不允許取消
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
              example:
                error:
                  code: "INVALID_ORDER_STATUS"
                  message: "訂單已發貨,無法取消"

        '404':
          $ref: '#/components/responses/NotFound'
```

### 3. Schema 定義

```yaml
components:
  schemas:
    # 通用錯誤響應
    ErrorResponse:
      type: object
      required:
        - error
      properties:
        error:
          type: object
          required:
            - code
            - message
          properties:
            code:
              type: string
              description: 錯誤代碼 (機器可讀)
              example: "INVALID_INPUT"
            message:
              type: string
              description: 錯誤訊息 (人類可讀)
              example: "請求參數驗證失敗"
            details:
              type: object
              description: 額外錯誤細節
              additionalProperties: true
            traceId:
              type: string
              format: uuid
              description: 追蹤ID,用於日誌查詢
              example: "550e8400-e29b-41d4-a716-446655440000"

    # 訂單創建請求
    CreateOrderRequest:
      type: object
      required:
        - items
        - shippingAddress
      properties:
        items:
          type: array
          minItems: 1
          maxItems: 100
          items:
            type: object
            required:
              - productId
              - quantity
            properties:
              productId:
                type: string
                pattern: '^prod_[a-zA-Z0-9]{10}$'
                example: "prod_abc123"
              quantity:
                type: integer
                minimum: 1
                maximum: 999
                example: 2
        shippingAddress:
          $ref: '#/components/schemas/Address'
        couponCode:
          type: string
          pattern: '^[A-Z0-9]{6,12}$'
          description: 優惠券代碼 (可選)
          example: "SAVE10"

    # 地址
    Address:
      type: object
      required:
        - recipientName
        - phone
        - address
        - postalCode
      properties:
        recipientName:
          type: string
          minLength: 1
          maxLength: 50
          example: "王小明"
        phone:
          type: string
          pattern: '^09[0-9]{8}$'
          example: "0912345678"
        address:
          type: string
          minLength: 1
          maxLength: 200
          example: "台北市信義區市府路1號"
        postalCode:
          type: string
          pattern: '^[0-9]{3,5}$'
          example: "110"

    # 訂單響應
    OrderResponse:
      type: object
      required:
        - orderId
        - status
        - totalAmount
        - createdAt
      properties:
        orderId:
          type: string
          example: "ord_abc123"
        status:
          type: string
          enum: [PENDING_PAYMENT, PAID, SHIPPING, COMPLETED, CANCELLED]
          example: "PENDING_PAYMENT"
        totalAmount:
          $ref: '#/components/schemas/Money'
        createdAt:
          type: string
          format: date-time
          example: "2025-10-13T10:30:00Z"
        paidAt:
          type: string
          format: date-time
          nullable: true
        paymentUrl:
          type: string
          format: uri
          description: 支付連結 (僅待支付訂單有此欄位)

    # 金額
    Money:
      type: object
      required:
        - amount
        - currency
      properties:
        amount:
          type: number
          format: double
          minimum: 0
          example: 1500.50
        currency:
          type: string
          enum: [TWD, USD, CNY]
          example: "TWD"

  # 可重用參數
  parameters:
    OrderIdParam:
      name: orderId
      in: path
      required: true
      description: 訂單ID
      schema:
        type: string
        pattern: '^ord_[a-zA-Z0-9]{10}$'
      example: ord_abc123

  # 可重用響應
  responses:
    BadRequest:
      description: 請求參數錯誤
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorResponse'
          example:
            error:
              code: "INVALID_INPUT"
              message: "請求參數驗證失敗"
              details:
                field: "items[0].quantity"
                constraint: "必須大於0"

    Unauthorized:
      description: 未認證或認證失敗
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorResponse'
          example:
            error:
              code: "UNAUTHORIZED"
              message: "請先登入"

    NotFound:
      description: 資源不存在
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorResponse'
          example:
            error:
              code: "NOT_FOUND"
              message: "訂單不存在"

    InternalServerError:
      description: 服務器內部錯誤
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorResponse'
          example:
            error:
              code: "INTERNAL_ERROR"
              message: "服務暫時不可用,請稍後重試"
              traceId: "550e8400-e29b-41d4-a716-446655440000"
```

### 4. 錯誤處理策略

#### 4.1 錯誤代碼分類

```markdown
| HTTP Status | 錯誤代碼類別 | 範例 | 處理建議 |
|-------------|--------------|------|----------|
| 400 | INVALID_INPUT_* | INVALID_INPUT_FORMAT | 檢查請求參數 |
| 401 | UNAUTHORIZED_* | UNAUTHORIZED_EXPIRED_TOKEN | 重新登入 |
| 403 | FORBIDDEN_* | FORBIDDEN_INSUFFICIENT_PERMISSION | 聯繫管理員 |
| 404 | NOT_FOUND_* | NOT_FOUND_RESOURCE | 確認資源ID |
| 409 | CONFLICT_* | CONFLICT_DUPLICATE_ORDER | 檢查重複提交 |
| 422 | BUSINESS_ERROR_* | BUSINESS_ERROR_INSUFFICIENT_STOCK | 業務約束 |
| 429 | RATE_LIMIT_* | RATE_LIMIT_EXCEEDED | 減少請求頻率 |
| 500 | INTERNAL_ERROR_* | INTERNAL_ERROR_DATABASE | 稍後重試 |
| 503 | SERVICE_UNAVAILABLE_* | SERVICE_UNAVAILABLE_MAINTENANCE | 等待恢復 |
```

#### 4.2 可重試與不可重試錯誤

```typescript
// 可重試錯誤 (客戶端應自動重試)
const RETRYABLE_ERROR_CODES = [
  'INTERNAL_ERROR_TIMEOUT',
  'INTERNAL_ERROR_DATABASE',
  'SERVICE_UNAVAILABLE_MAINTENANCE',
  'RATE_LIMIT_EXCEEDED' // 需指數退避
];

// 不可重試錯誤 (客戶端應提示用戶修正)
const NON_RETRYABLE_ERROR_CODES = [
  'INVALID_INPUT_FORMAT',
  'UNAUTHORIZED_INVALID_TOKEN',
  'NOT_FOUND_RESOURCE',
  'BUSINESS_ERROR_INSUFFICIENT_STOCK'
];
```

### 5. 版本控制策略

#### 5.1 版本演進規則

- **URL 版本**: `/api/v1/orders`, `/api/v2/orders`
  - 用於重大不相容變更
  - 舊版本維護至少 6 個月

- **向後相容變更** (無需升版本):
  - ✅ 新增可選欄位
  - ✅ 新增端點
  - ✅ 放寬驗證規則 (如放大數值範圍)

- **不相容變更** (需升版本):
  - ❌ 刪除欄位
  - ❌ 修改欄位類型
  - ❌ 修改端點 URL
  - ❌ 收緊驗證規則

#### 5.2 棄用流程

```yaml
paths:
  /orders/{orderId}/items:  # 舊端點
    get:
      deprecated: true
      description: |
        ⚠️ 已棄用,將於 2026-01-01 移除
        請改用 `/api/v2/orders/{orderId}` 取得完整訂單信息
      responses:
        '200':
          description: 成功
          headers:
            Deprecation:
              schema:
                type: string
                example: "true"
            Sunset:
              schema:
                type: string
                format: date
                example: "2026-01-01"
```

### 6. 安全設計

#### 6.1 認證方案

```yaml
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: |
        JWT Token 格式:
        ```json
        {
          "sub": "user_123",
          "role": "customer",
          "exp": 1672531200
        }
        ```

    apiKey:
      type: apiKey
      in: header
      name: X-API-Key
      description: 伺服器對伺服器調用使用 API Key
```

#### 6.2 授權控制

```yaml
paths:
  /admin/orders:
    get:
      tags:
        - Admin
      summary: 查詢所有訂單 (管理員)
      security:
        - bearerAuth: []
      x-required-role: admin  # 自定義擴展欄位
```

#### 6.3 輸入驗證

所有輸入必須驗證:
- **格式驗證**: 使用 JSON Schema 的 `pattern`, `format`
- **範圍驗證**: `minimum`, `maximum`, `minLength`, `maxLength`
- **業務驗證**: 在應用層執行 (如庫存檢查)

### 7. 合約測試

#### 7.1 Provider 測試 (服務提供方)

```typescript
// 使用 Pact 或類似工具
describe('Order API Contract', () => {
  it('POST /orders 應該符合 OpenAPI 規範', async () => {
    const response = await request(app)
      .post('/api/v1/orders')
      .set('Authorization', `Bearer ${validToken}`)
      .send(validCreateOrderRequest);

    expect(response.status).toBe(201);
    expect(response.body).toMatchSchema(orderResponseSchema);
  });

  it('GET /orders/{orderId} 404 應該返回標準錯誤格式', async () => {
    const response = await request(app)
      .get('/api/v1/orders/nonexistent')
      .set('Authorization', `Bearer ${validToken}`);

    expect(response.status).toBe(404);
    expect(response.body).toMatchSchema(errorResponseSchema);
    expect(response.body.error.code).toBe('NOT_FOUND');
  });
});
```

#### 7.2 Consumer 測試 (服務消費方)

```typescript
// 消費方根據 OpenAPI 生成 Mock Server
import { setupServer } from 'msw/node';
import { rest } from 'msw';

const server = setupServer(
  rest.post('/api/v1/orders', (req, res, ctx) => {
    return res(
      ctx.status(201),
      ctx.json({
        orderId: 'ord_mock123',
        status: 'PENDING_PAYMENT',
        // ... 根據 OpenAPI schema 生成
      })
    );
  })
);

beforeAll(() => server.listen());
afterAll(() => server.close());
```

## 蘇格拉底檢核

1. **一致性**:
   - 所有端點的錯誤響應格式是否一致?
   - 命名風格 (camelCase/snake_case) 是否統一?

2. **完整性**:
   - 是否包含所有可能的狀態碼?
   - 每個錯誤是否有明確的處理建議?

3. **版本演進**:
   - 新增欄位會破壞現有客戶端嗎?
   - 棄用流程是否給予足夠時間?

4. **安全性**:
   - 敏感欄位 (密碼、信用卡) 是否標記為 `writeOnly`?
   - 是否有速率限制?

5. **可測試性**:
   - 是否提供合約測試範例?
   - Mock 數據是否足夠真實?

## 輸出格式

- 主文件: `openapi.yaml` (OpenAPI 3.0 格式)
- 分模組: `openapi/orders.yaml`, `openapi/products.yaml`
- 遵循 VibeCoding_Workflow_Templates/06_api_design_specification.md

## 審查清單

- [ ] 所有端點有完整的請求/響應 Schema
- [ ] 錯誤響應遵循統一格式
- [ ] 所有欄位有明確的驗證規則
- [ ] 認證授權方案明確
- [ ] 版本控制策略清晰
- [ ] 提供合約測試範例
- [ ] OpenAPI 文件可通過驗證器 (如 Spectral)

## 關聯文件

- **架構設計**: 03-architecture-design-doc.md (Container Diagram)
- **模組規格**: 07_module_specification_and_tests.md (實作細節)
- **安全檢查**: 13_security_and_readiness_checklists.md (安全審查)

---

**記住**: API 是系統的契約,好的 API 設計讓前後端並行開發,讓集成測試有明確依據,讓文檔永不過時。
