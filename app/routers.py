from fastapi import APIRouter, HTTPException, Depends
from app.models import AddItemRequest, AddItemResponse
from app.orders import add_item_to_order

router = APIRouter(prefix="/api/v1/orders", tags=["orders"])

@router.post("/{order_id}/items", response_model=AddItemResponse)
async def add_order_item(order_id: int, request: AddItemRequest):
    try:
        result = await add_item_to_order(order_id, request.goods_id, request.quantity)
        return AddItemResponse(success=True, message="Товар добавлен", order_item_id=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))