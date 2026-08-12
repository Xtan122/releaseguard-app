from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.models import Order
from app.database.session import get_db
from app.metrics.prometheus import orders_created_total, orders_failed_total
from app.schemas.order import OrderCreate, OrderResponse

router = APIRouter()

@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, db: Annotated[Session, Depends(get_db)]):
    try:
        total_amount = sum(item.quantity * item.unit_price for item in order.items)
        
        new_order = Order(
            customer_id=order.customer_id,
            total=total_amount,
            items=[item.model_dump() for item in order.items]
        )

        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        
        orders_created_total.inc()

        return {
            "order_id": new_order.id,
            "status": new_order.status,
            "total": new_order.total,
            "version": new_order.version,
        }
    except Exception:
        orders_failed_total.inc()
        raise

@router.get("/")
def get_orders(db: Annotated[Session, Depends(get_db)]):
    orders = db.query(Order).all()
    return orders

@router.get("/{id}")
def get_order(id: int, db: Annotated[Session, Depends(get_db)]):
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {
        "order_id": order.id,
        "status": order.status,
        "total": order.total,
        "version": order.version,
    }