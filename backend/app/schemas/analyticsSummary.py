from pydantic import BaseModel

class AnalyticsSummary(BaseModel):
    total_customers:int
    total_products:int
    total_orders:int
    total_sales:float

    model_config={
        "from_attributes":True
    }
    # total_order_items:int
    # total_revenue:float