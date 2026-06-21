from fastapi import APIRouter,Depends,HTTPException

from typing import List
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.products import Product
from app.schemas.product import ProductCreate, ProductResponse



router=APIRouter(prefix="/products",tags=["Products"])



@router.post("/",response_model=ProductResponse)
def create_products(product:ProductCreate,db:Session=Depends(get_db)):
    new_product=Product(
        name=product.name,
        category=product.category,
        unit_price=product.unit_price
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product




@router.get("/",response_model=List[ProductResponse])
def get_products(db:Session=Depends(get_db)):
      response=db.query(Product).all()

      return response



@router.get("/{product_id}",response_model=ProductResponse)
def get_product_by_id(product_id:int,db:Session=Depends(get_db)):
       product=db.query(Product).filter(Product.id==product_id).first()


       if not product:
          raise HTTPException(status_code=404,detail="Product not found")


       return product




@router.delete("/{product_id}")
def delete_product(product_id:int,db:Session=Depends(get_db)):
       product=db.query(Product).filter(Product.id==product_id).first()


       if not product:
          raise HTTPException(status_code=404,detail="Product not found")


       db.delete(product)
       db.commit()


       return {"message":"Product deleted successfully"}