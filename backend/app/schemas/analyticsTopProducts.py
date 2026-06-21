from pydantic import BaseModel


class topProducts(BaseModel):
    product_name:str
    total_sales:float

    model_config={
        "from_attributes":True
    }
