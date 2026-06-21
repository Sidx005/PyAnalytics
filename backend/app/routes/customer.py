from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate,CustomerResponse
from typing import List
router=APIRouter(prefix="/customers",tags=["Customers"])


@router.post("/")
def create_customer(customer:CustomerCreate,db:Session=Depends(get_db)):

   new_customer=Customer(
    name=customer.name,
    email=customer.email,
    region=customer.region
   )

   db.add(new_customer)
   db.commit()
   db.refresh(new_customer)


   return new_customer


@router.get("/",response_model=List[CustomerResponse])
def get_customers(db:Session=Depends(get_db)):
    return db.query(Customer).all()