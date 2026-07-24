---
name: 10-backend-python-impl
description: "Python/FastAPI 後端實作 - 基於 DDD 與 Clean Architecture 生成代碼骨架"
stage: "Development"
template_ref: "07_module_specification_and_tests.md"
---

# 指令 (你是資深 Python 後端架構師)

基於 DDD 聚合設計與資料庫綱要,生成符合 Clean Architecture 的 Python/FastAPI 程式碼骨架。代碼需包含完整型別提示、Pydantic 模型、SQLAlchemy ORM 映射,並將職責清晰分離。

## 交付結構

### 1. 目錄結構 (Clean Architecture)

```
src/
└── {bounded_context}/          # 界限上下文名稱 (例如: order, product)
    ├── __init__.py
    ├── domain/                 # 領域層 - 純業務邏輯
    │   ├── __init__.py
    │   ├── models.py           # 聚合根、實體、值對象 (Pydantic)
    │   ├── events.py           # 領域事件
    │   ├── exceptions.py       # 領域異常
    │   └── repositories.py     # 倉儲接口 (ABC)
    ├── application/            # 應用層 - 用例編排
    │   ├── __init__.py
    │   ├── services.py         # 應用服務 (Use Cases)
    │   ├── commands.py         # 命令 DTO
    │   └── queries.py          # 查詢 DTO
    ├── infrastructure/         # 基礎設施層 - 外部實作
    │   ├── __init__.py
    │   ├── orm/
    │   │   ├── __init__.py
    │   │   ├── models.py       # SQLAlchemy ORM 模型
    │   │   └── mappers.py      # Domain Model <-> ORM 轉換
    │   ├── repositories/
    │   │   ├── __init__.py
    │   │   └── sqlalchemy_repository.py  # 倉儲實作
    │   └── event_bus.py        # 事件總線實作
    └── presentation/           # 表現層 - API 端點
        ├── __init__.py
        ├── api/
        │   ├── __init__.py
        │   ├── routes.py       # FastAPI Router
        │   ├── schemas.py      # API 請求/響應 Schema
        │   └── dependencies.py # 依賴注入
        └── cli/                # CLI 命令 (可選)
            └── __init__.py
```

### 2. 領域層 (Domain Layer)

#### 2.1 領域模型 (domain/models.py)

```python
"""
領域模型 - 使用 Pydantic 確保型別安全與驗證
"""
from __future__ import annotations
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, Field, validator, root_validator
from uuid import UUID, uuid4


class OrderStatus(str, Enum):
    """訂單狀態枚舉"""
    PENDING_PAYMENT = "PENDING_PAYMENT"
    PAID = "PAID"
    SHIPPING = "SHIPPING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Money(BaseModel):
    """金額值對象"""
    amount: Decimal = Field(..., ge=0, description="金額,必須 >= 0")
    currency: str = Field(default="TWD", regex="^[A-Z]{3}$")

    class Config:
        frozen = True  # 不可變

    def add(self, other: Money) -> Money:
        """加法"""
        if self.currency != other.currency:
            raise ValueError(f"不可操作不同幣別: {self.currency} vs {other.currency}")
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def multiply(self, factor: int) -> Money:
        """乘法"""
        if factor < 0:
            raise ValueError("倍數不可為負數")
        return Money(amount=self.amount * factor, currency=self.currency)

    @classmethod
    def zero(cls, currency: str = "TWD") -> Money:
        """創建零金額"""
        return cls(amount=Decimal("0"), currency=currency)


class Quantity(BaseModel):
    """數量值對象"""
    value: int = Field(..., ge=1, le=999, description="數量,範圍 1-999")

    class Config:
        frozen = True

    @validator('value')
    def validate_positive_integer(cls, v):
        if v <= 0:
            raise ValueError('數量必須大於 0')
        if v > 999:
            raise ValueError('數量不可超過 999')
        return v


class OrderItem(BaseModel):
    """訂單項目 - 實體 (Entity)"""
    id: UUID = Field(default_factory=uuid4)
    product_id: UUID
    product_name: str = Field(..., min_length=1, max_length=255)
    quantity: Quantity
    unit_price: Money
    subtotal: Money

    class Config:
        frozen = True  # 創建後不可變

    @root_validator
    def validate_subtotal(cls, values):
        """驗證小計 = 單價 * 數量"""
        quantity = values.get('quantity')
        unit_price = values.get('unit_price')
        subtotal = values.get('subtotal')

        if quantity and unit_price and subtotal:
            expected_subtotal = unit_price.multiply(quantity.value)
            if subtotal.amount != expected_subtotal.amount:
                raise ValueError(
                    f"小計錯誤: 預期 {expected_subtotal.amount}, 實際 {subtotal.amount}"
                )

        return values

    @classmethod
    def create(
        cls,
        product_id: UUID,
        product_name: str,
        quantity: int,
        unit_price: Money
    ) -> OrderItem:
        """工廠方法"""
        qty = Quantity(value=quantity)
        subtotal = unit_price.multiply(quantity)
        return cls(
            product_id=product_id,
            product_name=product_name,
            quantity=qty,
            unit_price=unit_price,
            subtotal=subtotal
        )


class Order(BaseModel):
    """訂單聚合根 (Aggregate Root)"""
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    status: OrderStatus = Field(default=OrderStatus.PENDING_PAYMENT)
    items: List[OrderItem] = Field(default_factory=list)
    total_amount: Money
    created_at: datetime = Field(default_factory=datetime.utcnow)
    paid_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    cancel_reason: Optional[str] = None
    version: int = Field(default=1, description="樂觀鎖版本號")

    # 領域事件 (不持久化)
    _domain_events: List[DomainEvent] = []

    class Config:
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True

    def __init__(self, **data):
        super().__init__(**data)
        self._domain_events = []

    # ===== 不變量驗證 =====

    def _validate_invariants(self) -> None:
        """驗證聚合不變量"""
        # 不變量 1: 訂單項不可為空
        if not self.items:
            raise DomainError("訂單至少需要包含一個商品")

        # 不變量 2: 總金額 = 所有項目小計之和
        calculated_total = Money.zero(self.total_amount.currency)
        for item in self.items:
            calculated_total = calculated_total.add(item.subtotal)

        if self.total_amount.amount != calculated_total.amount:
            raise DomainError(
                f"訂單總金額錯誤: 預期 {calculated_total.amount}, "
                f"實際 {self.total_amount.amount}"
            )

    # ===== 工廠方法 =====

    @classmethod
    def create(cls, user_id: UUID, items: List[OrderItem]) -> Order:
        """創建訂單"""
        if not items:
            raise DomainError("訂單至少需要包含一個商品")

        # 計算總金額
        currency = items[0].unit_price.currency
        total = Money.zero(currency)
        for item in items:
            if item.unit_price.currency != currency:
                raise DomainError("所有商品必須使用相同幣別")
            total = total.add(item.subtotal)

        order = cls(
            user_id=user_id,
            items=items,
            total_amount=total,
            status=OrderStatus.PENDING_PAYMENT
        )

        order._validate_invariants()
        order._add_domain_event(OrderCreatedEvent(
            order_id=order.id,
            user_id=order.user_id,
            total_amount=order.total_amount
        ))

        return order

    # ===== 領域方法 =====

    def pay(self, payment_id: UUID) -> None:
        """支付訂單"""
        if self.status != OrderStatus.PENDING_PAYMENT:
            raise DomainError(f"訂單狀態 {self.status} 不可支付")

        self.status = OrderStatus.PAID
        self.paid_at = datetime.utcnow()

        self._add_domain_event(OrderPaidEvent(
            order_id=self.id,
            payment_id=payment_id,
            paid_amount=self.total_amount
        ))

    def cancel(self, reason: str) -> None:
        """取消訂單"""
        if self.status in (OrderStatus.COMPLETED, OrderStatus.CANCELLED):
            raise DomainError(f"訂單狀態 {self.status} 不可取消")

        if not reason:
            raise DomainError("取消原因不可為空")

        self.status = OrderStatus.CANCELLED
        self.cancelled_at = datetime.utcnow()
        self.cancel_reason = reason

        self._add_domain_event(OrderCancelledEvent(
            order_id=self.id,
            reason=reason
        ))

    def complete(self) -> None:
        """完成訂單"""
        if self.status != OrderStatus.SHIPPING:
            raise DomainError(f"訂單狀態 {self.status} 不可完成")

        self.status = OrderStatus.COMPLETED

        self._add_domain_event(OrderCompletedEvent(
            order_id=self.id,
            user_id=self.user_id
        ))

    # ===== 領域事件管理 =====

    def _add_domain_event(self, event: DomainEvent) -> None:
        """添加領域事件"""
        self._domain_events.append(event)

    def get_domain_events(self) -> List[DomainEvent]:
        """獲取領域事件"""
        return self._domain_events.copy()

    def clear_domain_events(self) -> None:
        """清除領域事件"""
        self._domain_events.clear()
```

#### 2.2 領域事件 (domain/events.py)

```python
"""
領域事件 - 描述已發生的業務事實
"""
from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from .models import Money


class DomainEvent(BaseModel):
    """領域事件基類"""
    event_id: UUID = Field(default_factory=uuid4)
    occurred_on: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        frozen = True


class OrderCreatedEvent(DomainEvent):
    """訂單已創建事件"""
    order_id: UUID
    user_id: UUID
    total_amount: Money


class OrderPaidEvent(DomainEvent):
    """訂單已支付事件"""
    order_id: UUID
    payment_id: UUID
    paid_amount: Money


class OrderCancelledEvent(DomainEvent):
    """訂單已取消事件"""
    order_id: UUID
    reason: str


class OrderCompletedEvent(DomainEvent):
    """訂單已完成事件"""
    order_id: UUID
    user_id: UUID
```

#### 2.3 領域異常 (domain/exceptions.py)

```python
"""
領域異常 - 業務規則違反
"""

class DomainError(Exception):
    """領域異常基類"""
    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class OrderNotFoundError(DomainError):
    """訂單不存在"""
    pass


class InvalidOrderStateError(DomainError):
    """訂單狀態不合法"""
    pass


class InsufficientStockError(DomainError):
    """庫存不足"""
    pass
```

#### 2.4 倉儲接口 (domain/repositories.py)

```python
"""
倉儲接口 - 在領域層定義,基礎設施層實作
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from .models import Order, OrderStatus


class IOrderRepository(ABC):
    """訂單倉儲接口"""

    @abstractmethod
    async def find_by_id(self, order_id: UUID) -> Optional[Order]:
        """根據 ID 查找訂單"""
        pass

    @abstractmethod
    async def find_by_user_id(
        self,
        user_id: UUID,
        page: int = 1,
        page_size: int = 20
    ) -> List[Order]:
        """查找用戶的訂單列表"""
        pass

    @abstractmethod
    async def find_by_status(
        self,
        status: OrderStatus,
        page: int = 1,
        page_size: int = 20
    ) -> List[Order]:
        """根據狀態查找訂單"""
        pass

    @abstractmethod
    async def save(self, order: Order) -> None:
        """保存訂單 (新增或更新)"""
        pass

    @abstractmethod
    async def delete(self, order_id: UUID) -> None:
        """刪除訂單 (軟刪除)"""
        pass
```

### 3. 基礎設施層 (Infrastructure Layer)

#### 3.1 ORM 模型 (infrastructure/orm/models.py)

```python
"""
SQLAlchemy ORM 模型
"""
from sqlalchemy import (
    Column, String, Integer, Numeric, DateTime, ForeignKey, Enum as SQLEnum
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import declarative_base, relationship
import enum
from datetime import datetime
import uuid

Base = declarative_base()


class OrderStatusEnum(str, enum.Enum):
    PENDING_PAYMENT = "PENDING_PAYMENT"
    PAID = "PAID"
    SHIPPING = "SHIPPING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class OrderORM(Base):
    __tablename__ = "orders"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), nullable=False, index=True)
    status = Column(
        SQLEnum(OrderStatusEnum),
        nullable=False,
        default=OrderStatusEnum.PENDING_PAYMENT,
        index=True
    )
    total_amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), nullable=False, default="TWD")

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    paid_at = Column(DateTime, nullable=True)
    cancelled_at = Column(DateTime, nullable=True)
    cancel_reason = Column(String, nullable=True)

    version = Column(Integer, nullable=False, default=1)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 關聯
    items = relationship("OrderItemORM", back_populates="order", cascade="all, delete-orphan")


class OrderItemORM(Base):
    __tablename__ = "order_items"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(PG_UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False, index=True)
    product_id = Column(PG_UUID(as_uuid=True), nullable=False, index=True)
    product_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)
    subtotal = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), nullable=False, default="TWD")

    # 關聯
    order = relationship("OrderORM", back_populates="items")
```

#### 3.2 領域模型與 ORM 映射 (infrastructure/orm/mappers.py)

```python
"""
領域模型 <-> ORM 模型轉換
"""
from typing import List
from domain.models import Order, OrderItem, OrderStatus, Money, Quantity
from .models import OrderORM, OrderItemORM, OrderStatusEnum
from decimal import Decimal


class OrderMapper:
    """訂單映射器"""

    @staticmethod
    def to_domain(orm: OrderORM) -> Order:
        """ORM -> 領域模型"""
        items = [
            OrderItem(
                id=item_orm.id,
                product_id=item_orm.product_id,
                product_name=item_orm.product_name,
                quantity=Quantity(value=item_orm.quantity),
                unit_price=Money(amount=item_orm.unit_price, currency=item_orm.currency),
                subtotal=Money(amount=item_orm.subtotal, currency=item_orm.currency)
            )
            for item_orm in orm.items
        ]

        return Order(
            id=orm.id,
            user_id=orm.user_id,
            status=OrderStatus(orm.status.value),
            items=items,
            total_amount=Money(amount=orm.total_amount, currency=orm.currency),
            created_at=orm.created_at,
            paid_at=orm.paid_at,
            cancelled_at=orm.cancelled_at,
            cancel_reason=orm.cancel_reason,
            version=orm.version
        )

    @staticmethod
    def to_orm(domain: Order) -> OrderORM:
        """領域模型 -> ORM"""
        orm = OrderORM(
            id=domain.id,
            user_id=domain.user_id,
            status=OrderStatusEnum(domain.status.value),
            total_amount=domain.total_amount.amount,
            currency=domain.total_amount.currency,
            created_at=domain.created_at,
            paid_at=domain.paid_at,
            cancelled_at=domain.cancelled_at,
            cancel_reason=domain.cancel_reason,
            version=domain.version
        )

        orm.items = [
            OrderItemORM(
                id=item.id,
                product_id=item.product_id,
                product_name=item.product_name,
                quantity=item.quantity.value,
                unit_price=item.unit_price.amount,
                subtotal=item.subtotal.amount,
                currency=item.unit_price.currency
            )
            for item in domain.items
        ]

        return orm
```

#### 3.3 倉儲實作 (infrastructure/repositories/sqlalchemy_repository.py)

```python
"""
SQLAlchemy 倉儲實作
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from domain.repositories import IOrderRepository
from domain.models import Order, OrderStatus
from infrastructure.orm.models import OrderORM, OrderStatusEnum
from infrastructure.orm.mappers import OrderMapper


class SQLAlchemyOrderRepository(IOrderRepository):
    """訂單倉儲 SQLAlchemy 實作"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.mapper = OrderMapper()

    async def find_by_id(self, order_id: UUID) -> Optional[Order]:
        """根據 ID 查找訂單"""
        stmt = (
            select(OrderORM)
            .where(OrderORM.id == order_id)
            .options(selectinload(OrderORM.items))
        )
        result = await self.session.execute(stmt)
        orm = result.scalar_one_or_none()

        return self.mapper.to_domain(orm) if orm else None

    async def find_by_user_id(
        self,
        user_id: UUID,
        page: int = 1,
        page_size: int = 20
    ) -> List[Order]:
        """查找用戶的訂單列表"""
        offset = (page - 1) * page_size
        stmt = (
            select(OrderORM)
            .where(OrderORM.user_id == user_id)
            .options(selectinload(OrderORM.items))
            .order_by(OrderORM.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )
        result = await self.session.execute(stmt)
        orms = result.scalars().all()

        return [self.mapper.to_domain(orm) for orm in orms]

    async def find_by_status(
        self,
        status: OrderStatus,
        page: int = 1,
        page_size: int = 20
    ) -> List[Order]:
        """根據狀態查找訂單"""
        offset = (page - 1) * page_size
        stmt = (
            select(OrderORM)
            .where(OrderORM.status == OrderStatusEnum(status.value))
            .options(selectinload(OrderORM.items))
            .order_by(OrderORM.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )
        result = await self.session.execute(stmt)
        orms = result.scalars().all()

        return [self.mapper.to_domain(orm) for orm in orms]

    async def save(self, order: Order) -> None:
        """保存訂單"""
        # 檢查是否已存在
        existing = await self.session.get(OrderORM, order.id)

        if existing:
            # 更新 (樂觀鎖檢查)
            if existing.version != order.version:
                raise ConcurrencyError(f"訂單 {order.id} 已被其他事務修改")

            # 更新欄位
            orm = self.mapper.to_orm(order)
            orm.version = order.version + 1  # 遞增版本號

            await self.session.merge(orm)
        else:
            # 新增
            orm = self.mapper.to_orm(order)
            self.session.add(orm)

        await self.session.flush()

    async def delete(self, order_id: UUID) -> None:
        """刪除訂單 (實際刪除,也可改為軟刪除)"""
        stmt = select(OrderORM).where(OrderORM.id == order_id)
        result = await self.session.execute(stmt)
        orm = result.scalar_one_or_none()

        if orm:
            await self.session.delete(orm)
            await self.session.flush()


class ConcurrencyError(Exception):
    """並發衝突錯誤"""
    pass
```

### 4. 應用層 (Application Layer)

#### 4.1 命令 DTO (application/commands.py)

```python
"""
命令 DTO - 表現層 -> 應用層
"""
from pydantic import BaseModel, Field
from uuid import UUID
from typing import List


class CreateOrderItemCommand(BaseModel):
    product_id: UUID
    quantity: int = Field(..., ge=1, le=999)


class CreateOrderCommand(BaseModel):
    user_id: UUID
    items: List[CreateOrderItemCommand] = Field(..., min_items=1)


class PayOrderCommand(BaseModel):
    order_id: UUID
    payment_id: UUID


class CancelOrderCommand(BaseModel):
    order_id: UUID
    reason: str = Field(..., min_length=1, max_length=500)
```

#### 4.2 應用服務 (application/services.py)

```python
"""
應用服務 - 用例編排
"""
from uuid import UUID
from typing import List
from domain.repositories import IOrderRepository
from domain.models import Order, OrderItem, Money, Quantity
from domain.exceptions import OrderNotFoundError
from .commands import CreateOrderCommand, PayOrderCommand, CancelOrderCommand


class OrderApplicationService:
    """訂單應用服務"""

    def __init__(
        self,
        order_repo: IOrderRepository,
        product_repo: IProductRepository,  # 跨上下文依賴
        event_bus: IEventBus
    ):
        self.order_repo = order_repo
        self.product_repo = product_repo
        self.event_bus = event_bus

    async def create_order(self, command: CreateOrderCommand) -> UUID:
        """創建訂單用例"""
        # 1. 驗證商品存在性與庫存 (調用商品上下文)
        product_ids = [item.product_id for item in command.items]
        products = await self.product_repo.find_by_ids(product_ids)

        if len(products) != len(product_ids):
            raise ApplicationError("部分商品不存在")

        product_map = {p.id: p for p in products}

        # 2. 檢查庫存
        for item_cmd in command.items:
            product = product_map[item_cmd.product_id]
            if product.stock_quantity < item_cmd.quantity:
                raise InsufficientStockError(
                    f"商品 {product.name} 庫存不足",
                    details={
                        "product_id": str(item_cmd.product_id),
                        "requested": item_cmd.quantity,
                        "available": product.stock_quantity
                    }
                )

        # 3. 構建訂單項
        items = [
            OrderItem.create(
                product_id=item_cmd.product_id,
                product_name=product_map[item_cmd.product_id].name,
                quantity=item_cmd.quantity,
                unit_price=Money(
                    amount=product_map[item_cmd.product_id].price,
                    currency="TWD"
                )
            )
            for item_cmd in command.items
        ]

        # 4. 創建訂單聚合
        order = Order.create(user_id=command.user_id, items=items)

        # 5. 保存聚合
        await self.order_repo.save(order)

        # 6. 發布領域事件
        for event in order.get_domain_events():
            await self.event_bus.publish(event)
        order.clear_domain_events()

        return order.id

    async def pay_order(self, command: PayOrderCommand) -> None:
        """支付訂單用例"""
        # 1. 載入聚合
        order = await self.order_repo.find_by_id(command.order_id)
        if not order:
            raise OrderNotFoundError(f"訂單 {command.order_id} 不存在")

        # 2. 執行領域邏輯
        order.pay(command.payment_id)

        # 3. 保存聚合
        await self.order_repo.save(order)

        # 4. 發布領域事件
        for event in order.get_domain_events():
            await self.event_bus.publish(event)
        order.clear_domain_events()

    async def cancel_order(self, command: CancelOrderCommand) -> None:
        """取消訂單用例"""
        order = await self.order_repo.find_by_id(command.order_id)
        if not order:
            raise OrderNotFoundError(f"訂單 {command.order_id} 不存在")

        order.cancel(command.reason)

        await self.order_repo.save(order)

        for event in order.get_domain_events():
            await self.event_bus.publish(event)
        order.clear_domain_events()

    async def get_user_orders(
        self,
        user_id: UUID,
        page: int = 1,
        page_size: int = 20
    ) -> List[Order]:
        """查詢用戶訂單列表"""
        return await self.order_repo.find_by_user_id(user_id, page, page_size)


class ApplicationError(Exception):
    """應用層異常"""
    pass
```

### 5. 表現層 (Presentation Layer)

#### 5.1 API Schema (presentation/api/schemas.py)

```python
"""
API 請求/響應 Schema
"""
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import List


class CreateOrderItemRequest(BaseModel):
    product_id: UUID
    quantity: int = Field(..., ge=1, le=999)


class CreateOrderRequest(BaseModel):
    items: List[CreateOrderItemRequest] = Field(..., min_items=1)


class OrderItemResponse(BaseModel):
    id: UUID
    product_id: UUID
    product_name: str
    quantity: int
    unit_price: Decimal
    subtotal: Decimal
    currency: str


class OrderResponse(BaseModel):
    id: UUID
    user_id: UUID
    status: str
    items: List[OrderItemResponse]
    total_amount: Decimal
    currency: str
    created_at: datetime
    paid_at: datetime | None = None


class CancelOrderRequest(BaseModel):
    reason: str = Field(..., min_length=1, max_length=500)
```

#### 5.2 FastAPI Router (presentation/api/routes.py)

```python
"""
FastAPI 路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from typing import List

from application.services import OrderApplicationService
from application.commands import (
    CreateOrderCommand,
    PayOrderCommand,
    CancelOrderCommand
)
from .schemas import (
    CreateOrderRequest,
    OrderResponse,
    CancelOrderRequest
)
from .dependencies import get_order_service, get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OrderResponse)
async def create_order(
    request: CreateOrderRequest,
    current_user: UUID = Depends(get_current_user),
    service: OrderApplicationService = Depends(get_order_service)
):
    """創建訂單"""
    try:
        command = CreateOrderCommand(
            user_id=current_user,
            items=request.items
        )
        order_id = await service.create_order(command)

        # 查詢剛創建的訂單並返回
        orders = await service.get_user_orders(current_user, page=1, page_size=1)
        order = next((o for o in orders if o.id == order_id), None)

        return _to_order_response(order)

    except InsufficientStockError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "code": "INSUFFICIENT_STOCK",
                "message": str(e),
                "details": e.details
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": "INTERNAL_ERROR", "message": "服務暫時不可用"}
        )


@router.get("/", response_model=List[OrderResponse])
async def list_orders(
    page: int = 1,
    page_size: int = 20,
    current_user: UUID = Depends(get_current_user),
    service: OrderApplicationService = Depends(get_order_service)
):
    """查詢訂單列表"""
    orders = await service.get_user_orders(current_user, page, page_size)
    return [_to_order_response(order) for order in orders]


@router.delete("/{order_id}", status_code=status.HTTP_200_OK)
async def cancel_order(
    order_id: UUID,
    request: CancelOrderRequest,
    current_user: UUID = Depends(get_current_user),
    service: OrderApplicationService = Depends(get_order_service)
):
    """取消訂單"""
    try:
        command = CancelOrderCommand(order_id=order_id, reason=request.reason)
        await service.cancel_order(command)
        return {"message": "訂單已取消"}

    except OrderNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "訂單不存在"}
        )


def _to_order_response(order: Order) -> OrderResponse:
    """領域模型 -> API Response"""
    return OrderResponse(
        id=order.id,
        user_id=order.user_id,
        status=order.status.value,
        items=[
            OrderItemResponse(
                id=item.id,
                product_id=item.product_id,
                product_name=item.product_name,
                quantity=item.quantity.value,
                unit_price=item.unit_price.amount,
                subtotal=item.subtotal.amount,
                currency=item.unit_price.currency
            )
            for item in order.items
        ],
        total_amount=order.total_amount.amount,
        currency=order.total_amount.currency,
        created_at=order.created_at,
        paid_at=order.paid_at
    )
```

#### 5.3 依賴注入 (presentation/api/dependencies.py)

```python
"""
FastAPI 依賴注入
"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from infrastructure.database import get_db_session
from infrastructure.repositories.sqlalchemy_repository import SQLAlchemyOrderRepository
from application.services import OrderApplicationService


async def get_order_service(
    session: AsyncSession = Depends(get_db_session)
) -> OrderApplicationService:
    """獲取訂單應用服務"""
    order_repo = SQLAlchemyOrderRepository(session)
    product_repo = ...  # 商品倉儲
    event_bus = ...  # 事件總線

    return OrderApplicationService(order_repo, product_repo, event_bus)


async def get_current_user() -> UUID:
    """獲取當前用戶 (從 JWT Token 解析)"""
    # 實作略
    pass
```

## 蘇格拉底檢核

1. **依賴反轉**:
   - 應用層與領域層是否完全不依賴基礎設施層的具體實作?
   - 倉儲接口在領域層定義,實作在基礎設施層?

2. **領域純淨性**:
   - 領域模型是否不含任何資料庫、框架相關代碼?
   - 領域邏輯是否可脫離 FastAPI 與 SQLAlchemy 單獨測試?

3. **不變量保護**:
   - 聚合根是否在所有公開方法中強制執行不變量?
   - 值對象是否不可變 (frozen)?

4. **錯誤處理**:
   - 領域異常與應用異常是否明確區分?
   - API 層是否將領域異常轉換為適當的 HTTP 狀態碼?

5. **事件驅動**:
   - 領域事件是否描述過去已發生的事實 (過去式命名)?
   - 事件是否在聚合狀態變更後發布?

## 輸出格式

- Python 代碼使用 Black 格式化 (行長 88)
- 所有公開函式/類別需有 Docstring
- 使用 Type Hints (Python 3.10+)
- 遵循 PEP 8 規範

## 審查清單

- [ ] 目錄結構遵循 Clean Architecture 分層
- [ ] 領域模型使用 Pydantic 並包含驗證
- [ ] 值對象不可變 (Config.frozen = True)
- [ ] 聚合根保護不變量
- [ ] 倉儲接口在領域層定義
- [ ] ORM 模型與領域模型分離
- [ ] 有 Mapper 處理模型轉換
- [ ] 應用服務只負責用例編排
- [ ] API 層使用依賴注入
- [ ] 所有異步方法使用 async/await
- [ ] 包含完整型別提示

## 關聯文件

- **領域模型**: 04-ddd-aggregate-spec.md (聚合設計)
- **資料庫設計**: 09-database-schema-spec.md (ORM 映射依據)
- **API 設計**: 05-api-contract-spec.md (API Schema 依據)
- **測試規範**: 06-tdd-unit-spec.md (單元測試)

---

**記住**: Clean Architecture 的核心是依賴反轉,讓業務邏輯獨立於框架與基礎設施。領域層應該是純淨的,可在任何環境下測試與演進。
