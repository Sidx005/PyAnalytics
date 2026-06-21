from sqlalchemy import Column, Integer, Float, Date, ForeignKey

from app.database import Base


class Order(Base):
    __tablename__="orders"

    id=Column(Integer,primary_key=True,index=True)
    customer_id=Column(Integer,ForeignKey("customers.id"),nullable=False)
    # product_id=Column(Integer,ForeignKey("products.id"))
    total_amount=Column(Float,nullable=False)
    order_date=Column(Date,nullable=False)