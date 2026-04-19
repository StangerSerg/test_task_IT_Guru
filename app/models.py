from pydantic import BaseModel
from sqlalchemy import (Column,
                        Integer,
                        String,
                        Numeric,
                        ForeignKey,
                        DateTime,
                        text,
                        CheckConstraint,
                        )
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class AddItemRequest(BaseModel):
    goods_id: int
    quantity: int


class AddItemResponse(BaseModel):
    success: bool
    message: str
    order_item_id: int | None


class GoodsCategory(Base):
    __tablename__ = 'goods_categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    parent_id = Column(Integer, ForeignKey('goods_categories.id'))
    root_category_id = Column(Integer, ForeignKey('goods_categories.id'))

    parent = relationship("GoodsCategory", remote_side=[id], foreign_keys=[parent_id])
    root_category = relationship("GoodsCategory", remote_side=[id], foreign_keys=[root_category_id])
    children = relationship("GoodsCategory", back_populates="parent")
    goods = relationship("Goods", back_populates="category")


class Goods(Base):
    __tablename__ = 'goods'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    stock_quantity = Column(Integer, nullable=False, server_default='0')
    price = Column(Numeric(15, 2), nullable=False, server_default='0')
    category_id = Column(Integer, ForeignKey('goods_categories.id'))

    category = relationship("GoodsCategory", back_populates="goods")
    order_items = relationship("OrderGoods", back_populates="goods")

    __table_args__ = (
        CheckConstraint('stock_quantity >= 0', name='check_stock_positive'),
        CheckConstraint('price >= 0', name='check_price_positive'),
    )


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)

    orders = relationship("ClientOrder", back_populates="client")


class ClientOrder(Base):
    __tablename__ = 'client_orders'

    id = Column(Integer, primary_key=True)
    number = Column(String(100), nullable=False, unique=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    status = Column(String(20), nullable=False, server_default='pending')

    client = relationship("Client", back_populates="orders")
    order_goods = relationship("OrderGoods", back_populates="order", cascade="all, delete-orphan")


class OrderGoods(Base):
    __tablename__ = 'order_goods'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    client_order_id = Column(Integer, ForeignKey('client_orders.id'))
    goods_id = Column(Integer, ForeignKey('goods.id'))
    order_price = Column(Numeric(15, 2), nullable=False)
    order_quantity = Column(Integer, nullable=False)

    order = relationship("ClientOrder", back_populates="order_goods")
    goods = relationship("Goods", back_populates="order_items")

    __table_args__ = (
        CheckConstraint('order_quantity > 0', name='check_quantity_positive'),
    )