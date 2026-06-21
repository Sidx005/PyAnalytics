from typing import List
# from rich.status import status
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.customer import Customer
from app.models.products import Product

from app.schemas.orders import (
    OrderCreate,
    OrderResponse
)


router=APIRouter(prefix="/orders",tags=["Orders"])

@router.post("/",response_model=OrderResponse)
def create_order(order_data:OrderCreate,db:Session=Depends(get_db)):
    customer=(db.query(Customer).filter(Customer.id==order_data.customer_id).first())
    if not customer:
        raise HTTPException(status_code=404,detail="Customer not found")
    
    if not order_data.items:
        raise HTTPException(
            status_code=400,
            detail="Order must contain at least one item"
        )
    order=Order(
        customer_id=order_data.customer_id,
        order_date=date.today(),
        total_amount=0.0

    )

    db.add(order)
    db.commit()
    db.refresh(order)


    total_amount=0.0

    for item in order_data.items:
        product=db.query(Product).filter(Product.id==item.product_id).first()

        subtotal=(product.unit_price*item.quantity)
        total_amount+=subtotal
        order_item=OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            subtotal=subtotal
            # price=product.unit_price
        )
        db.add(order_item)

    order.total_amount=total_amount
    db.commit()
    db.refresh(order)

    return order





@router.get("/",response_model=List[OrderResponse])
def get_orders(db:Session=Depends(get_db)):
    return db.query(Order).all()



@router.get("/{order_id}",response_model=OrderResponse)
def get_order_by_id(order_id:int,db:Session=Depends(get_db)):
    order=db.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=404,detail="Order not found")
    return order



@router.delete("/{order_id}")
def delete_order(order_id:int,db:Session=Depends(get_db)):
    order=db.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=404,detail="Order not found")
    db.query(OrderItem).filter(OrderItem.order_id==order_id).delete()
    db.delete(order)
    db.commit()
    return {"message":"Order deleted successfully"}
