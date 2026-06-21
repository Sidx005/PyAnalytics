from pydantic import BaseModel
from datetime import datetime


class UploadResponse(BaseModel):
    id:int
    file_name:str
    status:str
    uploaded_at:datetime

    model_config={
        "from_attributes":True
    }



class UploadListResponse(BaseModel):
    id:int
    file_name:str
    status:str

    model_config={
        "from_attributes":True
    }