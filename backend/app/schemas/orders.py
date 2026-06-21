from typing import List
from pydantic import BaseModel
# BaseModel is used to create the schema for the order
# Explain how does BaseModel work? 
# It is a class that is used to create the schema for the order

class OrderItemCreate(BaseModel):
    product_id:int
    quantity:int




class OrderCreate(BaseModel):
    customer_id:int
    items:List[OrderItemCreate]



class OrderResponse(BaseModel):
    id:int
    customer_id:int
    total_amount:float


    model_config={
        "from_attributes":True
    }



