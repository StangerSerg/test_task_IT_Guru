from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import ClientOrder, Goods, OrderGoods


async def add_item_to_order(
        order_id: int,
        goods_id: int,
        quantity: int,
        db: AsyncSession
) -> int:
    # Валидация количества
    if quantity <= 0:
        raise ValueError("Количество должно быть положительным")

    # Валидация заказа
    order = await db.get(ClientOrder, order_id)
    if not order:
        raise ValueError(f"Заказ {order_id} не найден")

    # Валидация товара
    goods = await db.get(Goods, goods_id)
    if not goods:
        raise ValueError(f"Товар {goods_id} не найден")

    # Проверяем, есть ли такой товар в заказе
    result = await db.execute(
        select(OrderGoods).where(
            OrderGoods.client_order_id == order_id,
            OrderGoods.goods_id == goods_id
        )
    )
    order_item = result.scalar_one_or_none()

    # Проверяем остаток на складе
    new_quantity = quantity
    if order_item:
        new_quantity = order_item.order_quantity + quantity

    if new_quantity > goods.stock_quantity:
        raise ValueError(f"Не хватает товара. Доступно: {goods.stock_quantity}")

    # Добавляем или обновляем
    if order_item:
        order_item.order_quantity = new_quantity
    else:
        new_item = OrderGoods(
            client_order_id=order_id,
            goods_id=goods_id,
            order_price=goods.price,
            order_quantity=quantity
        )
        db.add(new_item)
        await db.flush()
        return new_item.id

    goods.stock_quantity -= quantity
    await db.flush()

    await db.flush()
    return order_item.id