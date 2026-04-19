from pydantic import BaseModel

class AddItemRequest(BaseModel):
    goods_id: int
    quantity: int

class AddItemResponse(BaseModel):
    success: bool
    message: str
    order_item_id: int | None