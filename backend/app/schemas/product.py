from pydantic import BaseModel

class ProductCreate(BaseModel):
    name:str
    category:str
    unit_price:float


class ProductResponse(BaseModel):
    id:int
    name:str
    category:str
    unit_price:float


    model_config={
        "from_attributes":True
    }