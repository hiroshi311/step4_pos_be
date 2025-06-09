from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    price: Decimal
    barcode: str

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 