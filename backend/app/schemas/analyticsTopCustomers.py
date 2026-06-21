from pydantic import BaseModel

class TopCustomer(BaseModel):
    customer_name:str
    total_spent:float

    model_config={
        "from_attributes":True
    }
