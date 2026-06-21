from pydantic import BaseModel
class CustomerCreate(BaseModel):
    name:str
    email:str
    region:str

class CustomerResponse(BaseModel):
    id:int
    name:str
    email:str
    region:str

    model_config={
        "from_attributes":True
    }