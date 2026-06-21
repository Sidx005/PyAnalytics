from fastapi import FastAPI,Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import Base,engine
from app.models.customer import Customer
from app.models.products import Product
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.upload_job import UploadJob
from app.models.analytics import Analytics

from app.database import get_db
from app.schemas.customer import CustomerCreate,CustomerResponse

from app.routes.customer import router as customer_router
from app.routes.product import router as product_router
from app.routes.orders import router as order_router
from app.routes.upload import router as upload_router
from app.routes.analyticsSummary import router as analytics_router
from app.routes.analyticsSalesByRegion import router as sales_by_region_router
from app.routes.analyticsTopProducts import router as top_products_router
from app.routes.analyticsTopcustomr import router as top_customers_router

Base.metadata.create_all(bind=engine)

app=FastAPI()


@app.get("/")

def root():
    return {"message":"Sales Dasahboard API"}


@app.get("/db-test")
def db_test():
    with engine.connect() as conn:
        result=conn.execute(text("SELECT 1"))

    return {"database":"connected"}

app.include_router(customer_router)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(upload_router)
app.include_router(analytics_router)
app.include_router(sales_by_region_router)
app.include_router(top_products_router)
app.include_router(top_customers_router)

# @app.post("/customers")
# def create_customer(customer:CustomerCreate,db:Session=Depends(get_db)):

#     new_customer=Customer(
#         name=customer.name,
#         email=customer.email,
#         region=customer.region
#     )

#     db.add(new_customer)
#     db.commit()
#     db.refresh(new_customer)

#     return new_customer



# @app.get("/customers")
# def get_customers(db:Session=Depends(get_db)):
#     customers=db.query(Customer).all()
#     return customers