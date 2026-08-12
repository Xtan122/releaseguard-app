
from pydantic import BaseModel


class OrderItem(BaseModel):
    product_id: str
    quantity: int
    unit_price: float

class OrderCreate(BaseModel):
    customer_id: str
    items: list[OrderItem]

class OrderResponse(BaseModel):
    order_id: int
    status: str
    total: float
    version: int