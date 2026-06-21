from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db


from app.models.customer import Customer
from app.models.products import Product
from app.models.order import Order


from app.schemas.analyticsSummary import AnalyticsSummary



router=APIRouter(prefix="/analytics",tags=["Analytics"])

@router.get("/summary",response_model=AnalyticsSummary)
def get_summary(db:Session=Depends(get_db)):
    total_customers=db.query(func.count(Customer.id)).scalar()
    total_products=db.query(func.count(Product.id)).scalar()
    total_orders=db.query(func.count(Order.id)).scalar()
    total_sales=db.query(func.sum(Order.total_amount)).scalar() or 0

    return AnalyticsSummary(
        total_customers=total_customers,
        total_products=total_products,
        total_orders=total_orders,
        total_sales=total_sales
    )