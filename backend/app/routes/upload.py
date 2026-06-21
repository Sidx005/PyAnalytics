from app.models.order_item import OrderItem
from datetime import date
from app.models.order import Order
from app.models.products import Product
from app.models.customer import Customer
from io import StringIO

import pandas as pd

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.upload_job import UploadJob

from app.schemas.uploadFile import UploadResponse,UploadListResponse

router=APIRouter(prefix="/upload",tags=["Upload"]
)


@router.post("/",response_model=UploadResponse)
async def upload_file(
    file:UploadFile=File(...),
    db:Session=Depends(get_db)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400,detail="Only csv file type is allowed")
    
    job=UploadJob(
        file_name=file.filename,status="PROCESSING"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    try:
        contents=await file.read()
        df=pd.read_csv(StringIO(contents.decode("utf-8")))
        required_columns={"customer_name","email","region","product_name","category","unit_price","quantity"}
        if not required_columns.issubset(df.columns):
            job.status="FAILED"

            db.commit()
            raise HTTPException(status_code=400,detail="Missing required columns")
        for row in df.itertuples():
            customer=db.query(Customer).filter(Customer.email==row.email).first()
            if not customer:
                customer=Customer(
                    name=row.customer_name,
                    email=row.email,
                    region=row.region
                )
                db.add(customer)
                db.flush()

            product=(db.query(Product).filter(Product.name==row.product_name).first())
            if not product:
                product=Product(
                    name=row.product_name,
                    category=row.category,
                    unit_price=row.unit_price
                )
                db.add(product)
                db.flush()


            subtotal=float(row.unit_price)*int(row.quantity)
            order=Order(
                customer_id=customer.id,
                total_amount=subtotal,
                order_date=date.today()
            )
            db.add(order)
            db.flush()

           
            order_item=OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=row.quantity,
                subtotal=subtotal
            )
            db.add(order_item)
            


        db.commit()
        job.status="COMPLETED"

        db.commit()
        db.refresh(job)

        return job
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        job.status="FAILED"
        db.commit()
        raise HTTPException(status_code=500,detail=str(e))

    return job
    
    
from typing import List


@router.get(
    "/",
    response_model=List[UploadListResponse]
)
def get_uploads(
    db: Session = Depends(get_db)
):

    uploads = (
        db.query(UploadJob)
        .order_by(
            UploadJob.uploaded_at.desc()
        )
        .all()
    )

    return uploads



@router.delete("/{job_id}")
def delete_upload(job_id:int,db:Session=Depends(get_db)):
    upload=db.query(UploadJob).filter(UploadJob.id==job_id).first()
    if not upload:
        raise HTTPException(status_code=404,detail="Upload not found")
    db.delete(upload)
    db.commit()
    return {"message":"Upload deleted successfully"}


@router.get("/{job_id}",response_model=UploadResponse)
def get_upload_by_id(job_id:int,db:Session=Depends(get_db)):
    upload=db.query(UploadJob).filter(UploadJob.id==job_id).first()
    if not upload:
        raise HTTPException(status_code=404,detail="Upload not found")
    return upload