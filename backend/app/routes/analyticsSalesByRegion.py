from typing import List
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db

from app.models.order import Order
from app.models.customer import Customer

from app.schemas.analyticsSalesByRegion import salesByRegion

router=APIRouter(prefix="/analytics",tags=["Analytics"])

@router.get("/sales-by-region",response_model=List[salesByRegion])
def get_sales_by_region(db:Session=Depends(get_db)):
    results=db.query(Customer.region,func.sum(Order.total_amount)).join(Order,Customer.id==Order.customer_id).group_by(Customer.region).all()
    return [{"region":region,"sales":sales}for region,sales in results]
