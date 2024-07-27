from datetime import date
from typing import Annotated, List
from fastapi import Form, UploadFile
from pydantic import BaseModel

class FormPayload(BaseModel):    
    name: str = Form(...)
    pdf: UploadFile = Form(...)
    address: str = Form(...)
    date: str = Form(...)
    favorites: List[str] = Form(...)    
    favorite: str = Form(...)
    


    