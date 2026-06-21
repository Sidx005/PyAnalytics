from pydantic import BaseModel

class salesByRegion(BaseModel):
    region:str
    sales:float

    model_config={
        "from_attributes":True
    }