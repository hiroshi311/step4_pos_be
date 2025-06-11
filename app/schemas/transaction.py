from pydantic import BaseModel
from typing import List
from datetime import datetime

class TransactionDetailBase(BaseModel):
    product_id: int

class TransactionDetailCreate(TransactionDetailBase):
    quantity: int = 1
    tax_cd: str = "10"  # デフォルトで10%

class TransactionDetailResponse(BaseModel):
    TRD_ID: int
    DTL_ID: int
    PRD_ID: int
    PRD_CODE: str
    PRD_NAME: str
    PRD_PRICE: float
    TAX_CD: str
    quantity: int

    class Config:
        from_attributes = True

class TransactionBase(BaseModel):
    total_amount: int
    total_amount_ex_tax: int
    payment_method: str

class TransactionCreate(BaseModel):
    emp_cd: str
    store_cd: str
    pos_no: str
    payment_method: str
    details: List[TransactionDetailCreate]

    @property
    def total_amount_ex_tax(self) -> float:
        # 税抜合計金額の計算
        return sum(detail.quantity * detail.price for detail in self.details)

    @property
    def total_amount(self) -> float:
        # 税込合計金額の計算（消費税10%）
        return self.total_amount_ex_tax * 1.1

class TransactionResponse(BaseModel):
    TRD_ID: int
    datetime: datetime
    employee_code: str
    store_code: str
    pos_no: str
    total_amount: float
    total_amount_ex_tax: float
    payment_method: str
    details: List[TransactionDetailResponse]

    class Config:
        from_attributes = True