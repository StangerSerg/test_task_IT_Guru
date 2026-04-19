from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import AddItemRequest, AddItemResponse
from app.orders import add_item_to_order
from app.database import get_db

router = APIRouter(prefix="/api/v1/orders", tags=["orders"])

@router.post("/{order_id}/items", response_model=AddItemResponse)
async def add_order_item(
    order_id: int,
    request: AddItemRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        item_id = await add_item_to_order(order_id, request.goods_id, request.quantity, db)
        return AddItemResponse(success=True, message="Товар добавлен", order_item_id=item_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))