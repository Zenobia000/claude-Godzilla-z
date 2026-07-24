---
name: 12-integration-contract-suite
description: "跨系統整合測試 - 合約測試、Provider/Consumer 驗證、失效注入"
stage: "Testing"
template_ref: "07_module_specification_and_tests.md"
---

# 指令 (你是整合測試架構師)

產出跨系統合約的規格與測試骨架,為每個介面提供 Provider/Consumer 測試與失效注入案例。確保系統間集成的穩定性與演進安全性。

## 交付結構

### 1. 合約索引 (Contract Registry)

```markdown
## 系統整合合約清單

| 合約ID | 類型 | Provider | Consumer | 版本 | 狀態 |
|--------|------|----------|----------|------|------|
| CONT-001 | REST API | 訂單服務 | 前端應用 | v1.0 | 活躍 |
| CONT-002 | REST API | 商品服務 | 訂單服務 | v1.0 | 活躍 |
| CONT-003 | Event | 訂單服務 | 通知服務 | v1.0 | 活躍 |
| CONT-004 | Event | 訂單服務 | 庫存服務 | v1.0 | 活躍 |
| CONT-005 | gRPC | 用戶服務 | 訂單服務 | v1.0 | 活躍 |

### 合約所有權
- **Provider**: 提供服務的系統,負責維護合約穩定性
- **Consumer**: 消費服務的系統,負責驗證合約滿足需求
```

### 2. REST API 合約測試 (使用 Pact)

#### 2.1 Consumer 測試 (訂單服務調用商品服務)

```typescript
// order-service/tests/pacts/product-service.consumer.test.ts
import { pactWith } from 'jest-pact';
import { Matchers } from '@pact-foundation/pact';
import { ProductServiceClient } from '@/clients/product-service';

const { like, eachLike, uuid, iso8601DateTime } = Matchers;

pactWith(
  {
    consumer: '訂單服務',
    provider: '商品服務',
    port: 8080,
  },
  (interaction) => {
    describe('商品服務 API 合約', () => {
      let productClient: ProductServiceClient;

      beforeEach(() => {
        productClient = new ProductServiceClient('http://localhost:8080');
      });

      describe('GET /products/:id - 查詢單一商品', () => {
        beforeEach(() => {
          interaction.addInteraction({
            state: '商品 prod_123 存在',
            uponReceiving: '查詢商品 prod_123 的請求',
            withRequest: {
              method: 'GET',
              path: '/api/v1/products/prod_123',
              headers: {
                Accept: 'application/json',
              },
            },
            willRespondWith: {
              status: 200,
              headers: {
                'Content-Type': 'application/json',
              },
              body: {
                id: 'prod_123',
                sku: like('SKU-001'),
                name: like('商品名稱'),
                price: like(1000),
                currency: like('TWD'),
                stock_quantity: like(50),
                is_active: like(true),
                created_at: iso8601DateTime(),
              },
            },
          });
        });

        it('應該返回商品信息', async () => {
          const product = await productClient.getProductById('prod_123');

          expect(product).toMatchObject({
            id: 'prod_123',
            sku: expect.any(String),
            name: expect.any(String),
            price: expect.any(Number),
            currency: 'TWD',
            stock_quantity: expect.any(Number),
            is_active: true,
          });
        });
      });

      describe('GET /products/:id - 商品不存在', () => {
        beforeEach(() => {
          interaction.addInteraction({
            state: '商品 prod_999 不存在',
            uponReceiving: '查詢不存在商品的請求',
            withRequest: {
              method: 'GET',
              path: '/api/v1/products/prod_999',
            },
            willRespondWith: {
              status: 404,
              headers: {
                'Content-Type': 'application/json',
              },
              body: {
                error: {
                  code: 'NOT_FOUND',
                  message: like('商品不存在'),
                },
              },
            },
          });
        });

        it('應該返回 404 錯誤', async () => {
          await expect(
            productClient.getProductById('prod_999')
          ).rejects.toThrow('商品不存在');
        });
      });

      describe('POST /products/batch - 批量查詢商品', () => {
        beforeEach(() => {
          interaction.addInteraction({
            state: '商品 prod_001 和 prod_002 存在',
            uponReceiving: '批量查詢商品的請求',
            withRequest: {
              method: 'POST',
              path: '/api/v1/products/batch',
              headers: {
                'Content-Type': 'application/json',
              },
              body: {
                product_ids: ['prod_001', 'prod_002'],
              },
            },
            willRespondWith: {
              status: 200,
              headers: {
                'Content-Type': 'application/json',
              },
              body: eachLike({
                id: uuid(),
                sku: like('SKU-001'),
                name: like('商品名稱'),
                price: like(1000),
                currency: like('TWD'),
                stock_quantity: like(50),
              }),
            },
          });
        });

        it('應該返回商品列表', async () => {
          const products = await productClient.getProductsByIds([
            'prod_001',
            'prod_002',
          ]);

          expect(products).toHaveLength(2);
          products.forEach((product) => {
            expect(product).toMatchObject({
              id: expect.any(String),
              sku: expect.any(String),
              name: expect.any(String),
              price: expect.any(Number),
            });
          });
        });
      });
    });
  }
);
```

#### 2.2 Provider 驗證 (商品服務驗證合約)

```typescript
// product-service/tests/pacts/provider-verification.test.ts
import { Verifier } from '@pact-foundation/pact';
import path from 'path';
import { setupTestDatabase, seedTestData } from './helpers';

describe('商品服務 - Provider 合約驗證', () => {
  let server: any;

  beforeAll(async () => {
    // 啟動測試服務器
    const app = await import('../../src/app');
    server = app.listen(8080);

    // 準備測試數據
    await setupTestDatabase();
  });

  afterAll(async () => {
    await server.close();
  });

  it('應該滿足所有 Consumer 的合約期望', () => {
    const options = {
      provider: '商品服務',
      providerBaseUrl: 'http://localhost:8080',

      // Pact Broker 配置
      pactBrokerUrl: 'https://pact-broker.example.com',
      pactBrokerToken: process.env.PACT_BROKER_TOKEN,

      // 發布驗證結果
      publishVerificationResult: true,
      providerVersion: process.env.GIT_COMMIT,

      // 狀態處理
      stateHandlers: {
        '商品 prod_123 存在': async () => {
          await seedTestData({
            products: [
              {
                id: 'prod_123',
                sku: 'SKU-001',
                name: '測試商品',
                price: 1000,
                currency: 'TWD',
                stock_quantity: 50,
                is_active: true,
              },
            ],
          });
        },
        '商品 prod_999 不存在': async () => {
          // 確保商品不存在
          await deleteProduct('prod_999');
        },
        '商品 prod_001 和 prod_002 存在': async () => {
          await seedTestData({
            products: [
              { id: 'prod_001', name: '商品1', price: 100 },
              { id: 'prod_002', name: '商品2', price: 200 },
            ],
          });
        },
      },
    };

    return new Verifier(options).verifyProvider();
  });
});
```

### 3. 異步事件合約測試 (Message Pact)

#### 3.1 Producer 測試 (訂單服務發布事件)

```typescript
// order-service/tests/pacts/order-events.producer.test.ts
import { MessageProviderPact, Matchers } from '@pact-foundation/pact';
import { OrderPaidEventPublisher } from '@/events/publishers';

const { like, uuid, iso8601DateTime } = Matchers;

describe('訂單服務 - 事件發布合約', () => {
  const provider = new MessageProviderPact({
    messageProviders: {
      'an OrderPaidEvent message': () => ({
        event_type: 'order.paid',
        event_id: uuid(),
        occurred_on: iso8601DateTime(),
        payload: {
          order_id: uuid(),
          user_id: uuid(),
          total_amount: like(1500),
          currency: like('TWD'),
          payment_id: uuid(),
          paid_at: iso8601DateTime(),
        },
      }),
    },
    provider: '訂單服務',
    pactBrokerUrl: 'https://pact-broker.example.com',
  });

  it('should publish OrderPaidEvent correctly', () => {
    return provider.verify();
  });
});
```

#### 3.2 Consumer 測試 (通知服務訂閱事件)

```typescript
// notification-service/tests/pacts/order-events.consumer.test.ts
import { MessageConsumerPact, Matchers } from '@pact-foundation/pact';
import { OrderPaidEventHandler } from '@/events/handlers';

const { like, uuid, iso8601DateTime } = Matchers;

describe('通知服務 - 訂閱訂單事件合約', () => {
  const messagePact = new MessageConsumerPact({
    consumer: '通知服務',
    provider: '訂單服務',
    dir: path.resolve(__dirname, '../pacts'),
  });

  describe('OrderPaidEvent', () => {
    it('should handle OrderPaidEvent correctly', async () => {
      await messagePact
        .given('an order has been paid')
        .expectsToReceive('an OrderPaidEvent message')
        .withContent({
          event_type: 'order.paid',
          event_id: uuid(),
          occurred_on: iso8601DateTime(),
          payload: {
            order_id: uuid(),
            user_id: uuid(),
            total_amount: like(1500),
            currency: like('TWD'),
            payment_id: uuid(),
            paid_at: iso8601DateTime(),
          },
        })
        .withMetadata({
          'content-type': 'application/json',
          routing_key: 'order.paid',
        })
        .verify(async (message) => {
          // 驗證 Handler 能正確處理事件
          const handler = new OrderPaidEventHandler();
          await handler.handle(message);

          // 驗證應該發送通知郵件
          expect(mockEmailService.send).toHaveBeenCalledWith(
            expect.objectContaining({
              to: expect.any(String),
              template: 'ORDER_PAID_CONFIRMATION',
              data: expect.objectContaining({
                order_id: message.payload.order_id,
              }),
            })
          );
        });
    });
  });
});
```

### 4. gRPC 合約測試

#### 4.1 定義 Proto 合約

```protobuf
// contracts/user-service.proto
syntax = "proto3";

package user;

service UserService {
  rpc GetUser(GetUserRequest) returns (User);
  rpc ValidateUser(ValidateUserRequest) returns (ValidateUserResponse);
}

message GetUserRequest {
  string user_id = 1;
}

message User {
  string id = 1;
  string email = 2;
  string first_name = 3;
  string last_name = 4;
  string role = 5;
}

message ValidateUserRequest {
  string user_id = 1;
  string required_role = 2;
}

message ValidateUserResponse {
  bool is_valid = 1;
  string reason = 2;
}
```

#### 4.2 gRPC Consumer 測試

```typescript
// order-service/tests/grpc/user-service.test.ts
import * as grpc from '@grpc/grpc-js';
import * as protoLoader from '@grpc/proto-loader';
import { UserServiceClient } from '@/grpc-clients/user-service';

describe('用戶服務 gRPC 合約', () => {
  let client: UserServiceClient;
  let mockServer: grpc.Server;

  beforeAll(() => {
    // 設置 Mock gRPC Server
    mockServer = new grpc.Server();
    const packageDefinition = protoLoader.loadSync('./contracts/user-service.proto');
    const proto = grpc.loadPackageDefinition(packageDefinition) as any;

    mockServer.addService(proto.user.UserService.service, {
      GetUser: (call: any, callback: any) => {
        if (call.request.user_id === 'user_123') {
          callback(null, {
            id: 'user_123',
            email: 'test@example.com',
            first_name: 'Test',
            last_name: 'User',
            role: 'customer',
          });
        } else {
          callback({
            code: grpc.status.NOT_FOUND,
            message: '用戶不存在',
          });
        }
      },
    });

    mockServer.bindAsync(
      '127.0.0.1:50051',
      grpc.ServerCredentials.createInsecure(),
      () => mockServer.start()
    );

    client = new UserServiceClient('127.0.0.1:50051');
  });

  afterAll(() => {
    mockServer.forceShutdown();
  });

  it('should get user by id', async () => {
    const user = await client.getUser('user_123');

    expect(user).toMatchObject({
      id: 'user_123',
      email: 'test@example.com',
      role: 'customer',
    });
  });

  it('should throw error for non-existent user', async () => {
    await expect(client.getUser('user_999')).rejects.toThrow('用戶不存在');
  });
});
```

### 5. 失效注入測試 (Failure Injection)

```typescript
// order-service/tests/integration/resilience.test.ts
import { OrderService } from '@/services/order-service';
import { mockProductServiceDown, mockPaymentTimeout } from './mocks';

describe('訂單服務 - 失效場景', () => {
  let orderService: OrderService;

  beforeEach(() => {
    orderService = new OrderService();
  });

  describe('依賴服務不可用', () => {
    it('商品服務宕機 - 應該返回友好錯誤', async () => {
      mockProductServiceDown(); // 模擬 503 錯誤

      await expect(
        orderService.createOrder({
          user_id: 'user_123',
          items: [{ product_id: 'prod_123', quantity: 1 }],
        })
      ).rejects.toThrow('商品服務暫時不可用,請稍後重試');

      // 驗證沒有創建不完整的訂單
      const orders = await orderService.getUserOrders('user_123');
      expect(orders).toHaveLength(0);
    });

    it('支付服務超時 - 應該回滾訂單狀態', async () => {
      mockPaymentTimeout(); // 模擬超時

      const orderId = await orderService.createOrder({
        user_id: 'user_123',
        items: [{ product_id: 'prod_123', quantity: 1 }],
      });

      await expect(orderService.payOrder(orderId, 'pay_123')).rejects.toThrow(
        '支付超時'
      );

      // 驗證訂單狀態回滾
      const order = await orderService.getOrder(orderId);
      expect(order.status).toBe('PENDING_PAYMENT');
    });
  });

  describe('網路抖動', () => {
    it('間歇性網路錯誤 - 應該自動重試', async () => {
      let attemptCount = 0;
      mockProductService.mockImplementation(() => {
        attemptCount++;
        if (attemptCount < 3) {
          throw new Error('ECONNRESET'); // 前兩次失敗
        }
        return { id: 'prod_123', price: 1000 }; // 第三次成功
      });

      const order = await orderService.createOrder({
        user_id: 'user_123',
        items: [{ product_id: 'prod_123', quantity: 1 }],
      });

      expect(order).toBeDefined();
      expect(attemptCount).toBe(3); // 驗證重試了3次
    });
  });

  describe('降級策略', () => {
    it('庫存服務不可用 - 應該降級為異步檢查', async () => {
      mockInventoryServiceDown();

      const order = await orderService.createOrder({
        user_id: 'user_123',
        items: [{ product_id: 'prod_123', quantity: 1 }],
      });

      // 訂單應該創建成功,但標記為需要庫存確認
      expect(order.status).toBe('PENDING_INVENTORY_CHECK');
      expect(order.notes).toContain('庫存異步驗證中');
    });
  });

  describe('速率限制', () => {
    it('超過 API 速率限制 - 應該使用指數退避重試', async () => {
      let callTimes: number[] = [];

      mockProductService.mockImplementation(() => {
        callTimes.push(Date.now());
        if (callTimes.length < 4) {
          throw new Error('Rate limit exceeded'); // 429
        }
        return { id: 'prod_123', price: 1000 };
      });

      await orderService.createOrder({
        user_id: 'user_123',
        items: [{ product_id: 'prod_123', quantity: 1 }],
      });

      // 驗證重試間隔遞增 (指數退避)
      expect(callTimes[1] - callTimes[0]).toBeGreaterThanOrEqual(1000); // 1s
      expect(callTimes[2] - callTimes[1]).toBeGreaterThanOrEqual(2000); // 2s
      expect(callTimes[3] - callTimes[2]).toBeGreaterThanOrEqual(4000); // 4s
    });
  });
});
```

### 6. 合約演進測試 (Contract Evolution)

```typescript
// tests/contract-evolution/backwards-compatibility.test.ts
describe('合約向後相容性', () => {
  it('v2 API 應該兼容 v1 客戶端', async () => {
    // v1 客戶端請求
    const v1Request = {
      method: 'POST',
      url: '/api/v2/orders',
      body: {
        user_id: 'user_123',
        items: [{ product_id: 'prod_123', quantity: 1 }],
        // v1 沒有 shipping_method 欄位
      },
    };

    const response = await fetch(v1Request);

    // v2 應該提供預設值,不報錯
    expect(response.status).toBe(201);
    const order = await response.json();
    expect(order.shipping_method).toBe('standard'); // 預設值
  });

  it('v1 API 應該忽略 v2 客戶端的新欄位', async () => {
    // v2 客戶端請求 (包含新欄位)
    const v2Request = {
      method: 'POST',
      url: '/api/v1/orders',
      body: {
        user_id: 'user_123',
        items: [{ product_id: 'prod_123', quantity: 1 }],
        shipping_method: 'express', // v1 不支持的新欄位
      },
    };

    const response = await fetch(v2Request);

    // v1 應該忽略未知欄位,不報錯
    expect(response.status).toBe(201);
  });
});
```

### 7. CI/CD 集成

```yaml
# .github/workflows/contract-tests.yml
name: Contract Tests

on: [push, pull_request]

jobs:
  consumer-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Consumer Tests
        run: npm run test:pact:consumer

      - name: Publish Pacts to Broker
        run: |
          npm run pact:publish
        env:
          PACT_BROKER_TOKEN: ${{ secrets.PACT_BROKER_TOKEN }}
          GIT_COMMIT: ${{ github.sha }}

  provider-verification:
    runs-on: ubuntu-latest
    needs: consumer-tests
    steps:
      - uses: actions/checkout@v3

      - name: Verify Provider Contracts
        run: npm run test:pact:provider
        env:
          PACT_BROKER_TOKEN: ${{ secrets.PACT_BROKER_TOKEN }}
          GIT_COMMIT: ${{ github.sha }}

      - name: Can I Deploy?
        run: |
          npx pact-broker can-i-deploy \
            --pacticipant="訂單服務" \
            --version=${{ github.sha }} \
            --to-environment=production
        env:
          PACT_BROKER_TOKEN: ${{ secrets.PACT_BROKER_TOKEN }}
```

## 蘇格拉底檢核

1. **合約完整性**:
   - 是否涵蓋所有系統間的介面?
   - 是否包含正常、異常、邊界情況?

2. **獨立性**:
   - Consumer 測試是否無需啟動 Provider?
   - Provider 驗證是否使用狀態處理器準備測試數據?

3. **演進安全性**:
   - 新版本是否向後相容?
   - 是否有防止破壞性變更的檢查?

4. **失效處理**:
   - 是否測試依賴服務不可用的情況?
   - 是否有降級與重試策略?

5. **CI/CD 集成**:
   - 合約測試是否在部署前執行?
   - 是否使用 Pact Broker 管理合約?

## 輸出格式

- 使用 Pact 規範的 Consumer-Driven Contracts
- gRPC 使用 Protocol Buffers 定義
- 測試使用 Jest + Pact Foundation 工具鏈

## 審查清單

- [ ] 所有跨系統介面有合約定義
- [ ] Consumer 測試覆蓋主要場景
- [ ] Provider 驗證使用狀態處理器
- [ ] 異步事件有 Message Pact 測試
- [ ] 失效注入測試涵蓋關鍵依賴
- [ ] 合約演進有向後相容性測試
- [ ] CI/CD 集成 Pact Broker
- [ ] 使用 can-i-deploy 檢查部署安全性

## 關聯文件

- **API 設計**: 05-api-contract-spec.md (OpenAPI 合約)
- **架構設計**: 03-architecture-design-doc.md (系統依賴關係)
- **測試規範**: 06-tdd-unit-spec.md (測試原則)

---

**記住**: 合約測試確保系統間集成的穩定性。Consumer-Driven Contracts 讓各系統獨立演進,失效注入測試確保韌性。在微服務架構中,合約測試是必不可少的安全網。
