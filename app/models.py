from pydantic import BaseModel
from sqlalchemy import (Column,
                        Integer,
                        String,
                        Numeric,
                        ForeignKey,
                        DateTime,
                        text,
                        )
from sqlalchemy.orm import declarative_base


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


class Goods(Base):
    __tablename__ = 'goods'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=0)
    price = Column(Numeric(15, 2), nullable=False, default=0)
    category_id = Column(Integer, ForeignKey('goods_categories.id'))


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)


class ClientOrder(Base):
    __tablename__ = 'client_orders'

    id = Column(Integer, primary_key=True)
    number = Column(String(100), nullable=False, unique=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    status = Column(String(20), nullable=False, default='pending')


class OrderGoods(Base):
    __tablename__ = 'order_goods'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    client_order_id = Column(Integer, ForeignKey('client_orders.id'))
    goods_id = Column(Integer, ForeignKey('goods.id'))
    order_price = Column(Numeric(15, 2), nullable=False)  # цена на момент заказа
    order_quantity = Column(Integer, nullable=False)