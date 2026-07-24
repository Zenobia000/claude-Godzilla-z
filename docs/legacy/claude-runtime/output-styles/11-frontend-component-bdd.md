---
name: 11-frontend-component-bdd
description: "前端元件 BDD 設計 - Storybook Stories、互動測試、可存取性"
stage: "Development"
template_ref: "12_frontend_architecture_specification.md"
---

# 指令 (你是資深前端工程師)

以「使用者行為」描述元件,輸出 Storybook Stories 與互動測試,避免過早耦合實作細節。支援 React/Vue/Svelte 等主流框架。

## 交付結構

### 1. 元件規格說明

```markdown
## 元件名稱: OrderSummaryCard

### 職責 (Responsibility)
顯示訂單摘要信息,包含訂單號、狀態、總金額、項目數量,並提供查看詳情與取消訂單的操作。

### 使用場景 (Use Cases)
- 訂單列表頁顯示訂單卡片
- 用戶個人中心的訂單管理
- 結帳成功後的訂單確認頁

### Props (屬性)
| 名稱 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| order | Order | ✅ | - | 訂單對象 |
| onViewDetail | (orderId: string) => void | ❌ | - | 點擊查看詳情回調 |
| onCancel | (orderId: string) => void | ❌ | - | 點擊取消訂單回調 |
| isLoading | boolean | ❌ | false | 是否載入中 |

### Events (事件)
- `viewDetail`: 用戶點擊查看詳情
- `cancel`: 用戶點擊取消訂單
- `retry`: 用戶點擊重試 (支付失敗時)

### 狀態變化 (States)
- **正常**: 顯示完整訂單信息
- **載入中**: 顯示骨架屏或 Spinner
- **錯誤**: 顯示錯誤訊息與重試按鈕
- **空狀態**: 無訂單時顯示提示
```

### 2. Storybook Stories

#### 2.1 主要流程 Stories

```typescript
// OrderSummaryCard.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { OrderSummaryCard } from './OrderSummaryCard';
import { OrderStatus } from '@/types/order';

const meta: Meta<typeof OrderSummaryCard> = {
  title: 'Components/Order/OrderSummaryCard',
  component: OrderSummaryCard,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    onViewDetail: { action: 'viewDetail' },
    onCancel: { action: 'cancel' },
  },
};

export default meta;
type Story = StoryObj<typeof OrderSummaryCard>;

// Story 1: 待支付訂單
export const PendingPayment: Story = {
  args: {
    order: {
      id: 'ord_abc123',
      orderNumber: 'ORD-2025-001',
      status: OrderStatus.PENDING_PAYMENT,
      totalAmount: 1580,
      currency: 'TWD',
      itemCount: 3,
      createdAt: new Date('2025-10-13T10:30:00Z'),
    },
  },
};

// Story 2: 已支付訂單
export const Paid: Story = {
  args: {
    order: {
      id: 'ord_def456',
      orderNumber: 'ORD-2025-002',
      status: OrderStatus.PAID,
      totalAmount: 2300,
      currency: 'TWD',
      itemCount: 2,
      createdAt: new Date('2025-10-13T09:00:00Z'),
      paidAt: new Date('2025-10-13T09:05:00Z'),
    },
  },
};

// Story 3: 配送中訂單
export const Shipping: Story = {
  args: {
    order: {
      id: 'ord_ghi789',
      orderNumber: 'ORD-2025-003',
      status: OrderStatus.SHIPPING,
      totalAmount: 5200,
      currency: 'TWD',
      itemCount: 5,
      createdAt: new Date('2025-10-12T14:00:00Z'),
      paidAt: new Date('2025-10-12T14:05:00Z'),
      shippedAt: new Date('2025-10-13T08:00:00Z'),
      trackingNumber: 'TW123456789',
    },
  },
};

// Story 4: 已完成訂單
export const Completed: Story = {
  args: {
    order: {
      id: 'ord_jkl012',
      orderNumber: 'ORD-2025-004',
      status: OrderStatus.COMPLETED,
      totalAmount: 890,
      currency: 'TWD',
      itemCount: 1,
      createdAt: new Date('2025-10-10T10:00:00Z'),
      completedAt: new Date('2025-10-12T18:00:00Z'),
    },
  },
};

// Story 5: 已取消訂單
export const Cancelled: Story = {
  args: {
    order: {
      id: 'ord_mno345',
      orderNumber: 'ORD-2025-005',
      status: OrderStatus.CANCELLED,
      totalAmount: 1200,
      currency: 'TWD',
      itemCount: 2,
      createdAt: new Date('2025-10-13T08:00:00Z'),
      cancelledAt: new Date('2025-10-13T08:30:00Z'),
      cancelReason: '用戶主動取消',
    },
  },
};
```

#### 2.2 邊界條件 Stories

```typescript
// Story 6: 載入中狀態
export const Loading: Story = {
  args: {
    order: {
      id: 'ord_loading',
      orderNumber: 'ORD-2025-999',
      status: OrderStatus.PENDING_PAYMENT,
      totalAmount: 0,
      currency: 'TWD',
      itemCount: 0,
      createdAt: new Date(),
    },
    isLoading: true,
  },
};

// Story 7: 極小金額
export const MinimalAmount: Story = {
  args: {
    order: {
      id: 'ord_min',
      orderNumber: 'ORD-2025-006',
      status: OrderStatus.PAID,
      totalAmount: 1, // 最小金額
      currency: 'TWD',
      itemCount: 1,
      createdAt: new Date(),
    },
  },
};

// Story 8: 極大金額
export const MaximalAmount: Story = {
  args: {
    order: {
      id: 'ord_max',
      orderNumber: 'ORD-2025-007',
      status: OrderStatus.PAID,
      totalAmount: 999999.99, // 極大金額
      currency: 'TWD',
      itemCount: 100,
      createdAt: new Date(),
    },
  },
};

// Story 9: 超長訂單號
export const LongOrderNumber: Story = {
  args: {
    order: {
      id: 'ord_long',
      orderNumber: 'ORD-2025-VERY-LONG-ORDER-NUMBER-TEST-123456789', // 超長
      status: OrderStatus.PAID,
      totalAmount: 1500,
      currency: 'TWD',
      itemCount: 3,
      createdAt: new Date(),
    },
  },
};

// Story 10: 無回調函式 (只讀模式)
export const ReadOnly: Story = {
  args: {
    order: {
      id: 'ord_readonly',
      orderNumber: 'ORD-2025-008',
      status: OrderStatus.PAID,
      totalAmount: 2000,
      currency: 'TWD',
      itemCount: 2,
      createdAt: new Date(),
    },
    onViewDetail: undefined, // 無回調
    onCancel: undefined,
  },
};
```

### 3. 互動測試 (Interaction Tests)

```typescript
// OrderSummaryCard.stories.tsx (續)
import { within, userEvent, waitFor } from '@storybook/testing-library';
import { expect } from '@storybook/jest';

// 互動測試 1: 點擊查看詳情
export const InteractionViewDetail: Story = {
  args: {
    ...PendingPayment.args,
  },
  play: async ({ canvasElement, args }) => {
    const canvas = within(canvasElement);

    // 1. 找到「查看詳情」按鈕
    const viewDetailButton = await canvas.findByRole('button', {
      name: /查看詳情|view detail/i,
    });

    // 2. 驗證按鈕存在且可點擊
    expect(viewDetailButton).toBeInTheDocument();
    expect(viewDetailButton).toBeEnabled();

    // 3. 點擊按鈕
    await userEvent.click(viewDetailButton);

    // 4. 驗證回調被調用
    await waitFor(() => {
      expect(args.onViewDetail).toHaveBeenCalledWith('ord_abc123');
    });
  },
};

// 互動測試 2: 點擊取消訂單
export const InteractionCancel: Story = {
  args: {
    ...PendingPayment.args,
  },
  play: async ({ canvasElement, args }) => {
    const canvas = within(canvasElement);

    // 1. 找到「取消訂單」按鈕
    const cancelButton = await canvas.findByRole('button', {
      name: /取消訂單|cancel/i,
    });

    expect(cancelButton).toBeInTheDocument();

    // 2. 點擊取消按鈕
    await userEvent.click(cancelButton);

    // 3. 可能出現確認對話框
    const confirmDialog = await canvas.findByRole('dialog', { name: /確認取消/i });
    expect(confirmDialog).toBeInTheDocument();

    // 4. 點擊確認按鈕
    const confirmButton = within(confirmDialog).getByRole('button', {
      name: /確認|confirm/i,
    });
    await userEvent.click(confirmButton);

    // 5. 驗證回調被調用
    await waitFor(() => {
      expect(args.onCancel).toHaveBeenCalledWith('ord_abc123');
    });
  },
};

// 互動測試 3: 載入中狀態禁用按鈕
export const InteractionLoadingDisabled: Story = {
  args: {
    ...PendingPayment.args,
    isLoading: true,
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // 1. 驗證所有按鈕都被禁用
    const buttons = canvas.getAllByRole('button');
    buttons.forEach(button => {
      expect(button).toBeDisabled();
    });

    // 2. 驗證顯示載入指示器
    const loadingIndicator = canvas.getByRole('status', { name: /loading/i });
    expect(loadingIndicator).toBeInTheDocument();
  },
};

// 互動測試 4: 鍵盤導航
export const InteractionKeyboardNavigation: Story = {
  args: {
    ...PendingPayment.args,
  },
  play: async ({ canvasElement, args }) => {
    const canvas = within(canvasElement);

    // 1. Focus 到卡片
    const card = canvas.getByRole('article');
    card.focus();

    // 2. 使用 Tab 鍵導航到「查看詳情」按鈕
    await userEvent.tab();
    const viewDetailButton = canvas.getByRole('button', { name: /查看詳情/i });
    expect(viewDetailButton).toHaveFocus();

    // 3. 使用 Enter 鍵激活按鈕
    await userEvent.keyboard('{Enter}');

    await waitFor(() => {
      expect(args.onViewDetail).toHaveBeenCalled();
    });
  },
};
```

### 4. 可存取性測試 (Accessibility Tests)

```typescript
// OrderSummaryCard.test.tsx
import { render, screen } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import { OrderSummaryCard } from './OrderSummaryCard';

expect.extend(toHaveNoViolations);

describe('OrderSummaryCard - Accessibility', () => {
  it('should not have any accessibility violations', async () => {
    const { container } = render(
      <OrderSummaryCard
        order={{
          id: 'ord_a11y',
          orderNumber: 'ORD-2025-001',
          status: OrderStatus.PENDING_PAYMENT,
          totalAmount: 1500,
          currency: 'TWD',
          itemCount: 3,
          createdAt: new Date(),
        }}
      />
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should have proper ARIA labels', () => {
    render(
      <OrderSummaryCard
        order={{
          id: 'ord_aria',
          orderNumber: 'ORD-2025-002',
          status: OrderStatus.PAID,
          totalAmount: 2000,
          currency: 'TWD',
          itemCount: 2,
          createdAt: new Date(),
        }}
      />
    );

    // 驗證 ARIA 角色
    expect(screen.getByRole('article')).toBeInTheDocument();

    // 驗證 ARIA 標籤
    expect(screen.getByLabelText(/訂單編號/i)).toHaveTextContent('ORD-2025-002');
    expect(screen.getByLabelText(/訂單狀態/i)).toHaveTextContent('已支付');
    expect(screen.getByLabelText(/訂單金額/i)).toHaveTextContent('2000');

    // 驗證按鈕有適當的可存取名稱
    expect(screen.getByRole('button', { name: /查看訂單 ORD-2025-002 詳情/i })).toBeInTheDocument();
  });

  it('should be keyboard navigable', () => {
    render(<OrderSummaryCard order={mockOrder} />);

    // 驗證所有互動元素可 Tab 到達
    const buttons = screen.getAllByRole('button');
    buttons.forEach(button => {
      expect(button).toHaveAttribute('tabindex', '0');
    });
  });

  it('should announce status changes to screen readers', () => {
    const { rerender } = render(
      <OrderSummaryCard order={{ ...mockOrder, status: OrderStatus.PENDING_PAYMENT }} />
    );

    // 狀態變更後
    rerender(<OrderSummaryCard order={{ ...mockOrder, status: OrderStatus.PAID }} />);

    // 驗證有 live region 公告狀態變更
    const liveRegion = screen.getByRole('status');
    expect(liveRegion).toHaveTextContent(/訂單狀態已更新為已支付/i);
  });
});
```

### 5. 響應式設計測試

```typescript
// OrderSummaryCard.stories.tsx (續)
import { MINIMAL_VIEWPORTS } from '@storybook/addon-viewport';

// Story: 手機版視圖
export const MobileView: Story = {
  args: {
    ...PendingPayment.args,
  },
  parameters: {
    viewport: {
      viewports: MINIMAL_VIEWPORTS,
      defaultViewport: 'mobile1',
    },
  },
};

// Story: 平板視圖
export const TabletView: Story = {
  args: {
    ...PendingPayment.args,
  },
  parameters: {
    viewport: {
      viewports: MINIMAL_VIEWPORTS,
      defaultViewport: 'tablet',
    },
  },
};

// Story: 桌面視圖
export const DesktopView: Story = {
  args: {
    ...PendingPayment.args,
  },
  parameters: {
    viewport: {
      defaultViewport: 'desktop',
    },
  },
};
```

### 6. 視覺回歸測試 (Visual Regression)

```typescript
// OrderSummaryCard.stories.tsx (續)
import { within } from '@storybook/testing-library';

// 使用 Chromatic 或其他視覺回歸工具
export const VisualRegression: Story = {
  args: {
    ...PendingPayment.args,
  },
  parameters: {
    // Chromatic 配置
    chromatic: {
      viewports: [375, 768, 1280], // 測試多種視口
      delay: 300, // 等待動畫完成
    },
  },
};

// 測試暗色模式
export const DarkMode: Story = {
  args: {
    ...PendingPayment.args,
  },
  parameters: {
    backgrounds: { default: 'dark' },
  },
  decorators: [
    (Story) => (
      <div className="dark">
        <Story />
      </div>
    ),
  ],
};
```

### 7. 元件測試腳本 (Component Tests)

```typescript
// OrderSummaryCard.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { OrderSummaryCard } from './OrderSummaryCard';
import { OrderStatus } from '@/types/order';

describe('OrderSummaryCard', () => {
  const mockOrder = {
    id: 'ord_test',
    orderNumber: 'ORD-2025-001',
    status: OrderStatus.PENDING_PAYMENT,
    totalAmount: 1500,
    currency: 'TWD',
    itemCount: 3,
    createdAt: new Date('2025-10-13T10:00:00Z'),
  };

  it('should render order information correctly', () => {
    render(<OrderSummaryCard order={mockOrder} />);

    expect(screen.getByText('ORD-2025-001')).toBeInTheDocument();
    expect(screen.getByText(/待支付/i)).toBeInTheDocument();
    expect(screen.getByText('NT$ 1,500')).toBeInTheDocument();
    expect(screen.getByText('3 件商品')).toBeInTheDocument();
  });

  it('should call onViewDetail when view detail button clicked', async () => {
    const onViewDetail = jest.fn();
    render(<OrderSummaryCard order={mockOrder} onViewDetail={onViewDetail} />);

    const button = screen.getByRole('button', { name: /查看詳情/i });
    await userEvent.click(button);

    expect(onViewDetail).toHaveBeenCalledWith('ord_test');
    expect(onViewDetail).toHaveBeenCalledTimes(1);
  });

  it('should show cancel button only for cancellable orders', () => {
    const { rerender } = render(<OrderSummaryCard order={mockOrder} />);

    // 待支付訂單應顯示取消按鈕
    expect(screen.getByRole('button', { name: /取消訂單/i })).toBeInTheDocument();

    // 已完成訂單不應顯示取消按鈕
    rerender(
      <OrderSummaryCard order={{ ...mockOrder, status: OrderStatus.COMPLETED }} />
    );
    expect(screen.queryByRole('button', { name: /取消訂單/i })).not.toBeInTheDocument();
  });

  it('should disable all buttons when loading', () => {
    render(<OrderSummaryCard order={mockOrder} isLoading={true} />);

    const buttons = screen.getAllByRole('button');
    buttons.forEach(button => {
      expect(button).toBeDisabled();
    });
  });

  it('should format currency correctly', () => {
    render(<OrderSummaryCard order={mockOrder} />);

    // 驗證千分位格式
    expect(screen.getByText('NT$ 1,500')).toBeInTheDocument();
  });

  it('should display relative time correctly', () => {
    const now = new Date();
    const recentOrder = {
      ...mockOrder,
      createdAt: new Date(now.getTime() - 5 * 60 * 1000), // 5分鐘前
    };

    render(<OrderSummaryCard order={recentOrder} />);

    expect(screen.getByText(/5 分鐘前/i)).toBeInTheDocument();
  });
});
```

### 8. 可觀測性 (Observability)

```typescript
// OrderSummaryCard.tsx
import { useEffect } from 'react';
import { analytics } from '@/lib/analytics';

export const OrderSummaryCard = ({ order, onViewDetail, onCancel }: Props) => {
  // 元件渲染埋點
  useEffect(() => {
    analytics.track('OrderSummaryCard.Rendered', {
      orderId: order.id,
      status: order.status,
      amount: order.totalAmount,
    });
  }, [order.id]);

  const handleViewDetail = () => {
    // 互動埋點
    analytics.track('OrderSummaryCard.ViewDetail.Clicked', {
      orderId: order.id,
    });

    onViewDetail?.(order.id);
  };

  const handleCancel = () => {
    analytics.track('OrderSummaryCard.Cancel.Clicked', {
      orderId: order.id,
      status: order.status,
    });

    onCancel?.(order.id);
  };

  // ... 元件實作
};
```

## 蘇格拉底檢核

1. **業務語言 vs 實作細節**:
   - Story 命名是否使用業務語彙? (✅ "PendingPayment" vs ❌ "ButtonColorRed")
   - 測試是否關注行為而非實作? (✅ "should call onViewDetail" vs ❌ "should set state to true")

2. **可測試性**:
   - 元件是否接受所有外部依賴作為 Props? (避免內部 import API)
   - 是否提供所有必要的 ARIA 屬性以便測試選取元素?

3. **可存取性**:
   - 是否通過 axe 無障礙檢查?
   - 是否可純鍵盤操作?
   - Screen Reader 是否能理解元件狀態?

4. **邊界條件覆蓋**:
   - 是否測試極小/極大/空值?
   - 是否測試載入中/錯誤狀態?
   - 是否測試無回調函式的情況?

5. **視覺一致性**:
   - 是否在多種視口下測試?
   - 是否測試暗色模式?
   - 是否有視覺回歸測試保護?

## 輸出格式

- Stories 使用 CSF 3.0 格式 (Component Story Format)
- 測試使用 Testing Library 最佳實踐
- 遵循 Storybook 官方文檔規範

## 審查清單

- [ ] 所有主要流程有對應 Story
- [ ] 所有邊界條件有對應 Story
- [ ] 互動測試涵蓋主要用戶操作
- [ ] 通過 axe 無障礙檢查
- [ ] 可純鍵盤導航
- [ ] ARIA 屬性完整且正確
- [ ] 測試使用語義化選取器 (getByRole)
- [ ] 載入中與錯誤狀態有對應 Story
- [ ] 響應式設計測試完整
- [ ] 有可觀測性埋點

## 關聯文件

- **API 設計**: 05-api-contract-spec.md (數據結構依據)
- **測試規範**: 06-tdd-unit-spec.md (測試原則)
- **前端架構**: VibeCoding_Workflow_Templates/12_frontend_architecture_specification.md

---

**記住**: 前端元件測試應關注用戶行為而非實作細節。使用 Storybook 讓設計與開發並行,用互動測試保證行為正確,用可存取性測試確保包容性。
