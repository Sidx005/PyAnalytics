from app.models.order_item import OrderItem
from typing import List
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db

from app.models.order import Order
from app.models.products import Product

from app.schemas.analyticsTopProducts import topProducts

router=APIRouter(prefix="/analytics",tags=["Analytics"])
@router.get("/top-products",response_model=List[topProducts])
def get_top_Products(db:Session=Depends(get_db)):
    results=db.query(Product.name,func.sum(OrderItem.quantity)).join(OrderItem,Product.id==OrderItem.product_id).group_by(Product.name).order_by(func.sum(OrderItem.quantity).desc()).all()
    return [{"product_name":product_name,"total_sales":total_sales} for product_name,total_sales in results]
