from typing import List
from app.models.order import Order
from sqlalchemy import func
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.customer import Customer
from app.schemas.analyticsTopCustomers import TopCustomer


# from pyparsing import results
from sqlalchemy.orm.session import Session

router=APIRouter(prefix="/analytics",tags=["Analytics"])
@router.get("/top-customers",response_model=List[TopCustomer])
def top_Customers(db:Session=Depends(get_db)):
    results=db.query(Customer.name,func.sum(Order.total_amount)).join(Order,Customer.id==Order.customer_id).group_by(Customer.name).order_by(func.sum(Order.total_amount).desc()).all()

    return [{"customer_name":customer_name,"total_spent":total_spent} for customer_name,total_spent in results]