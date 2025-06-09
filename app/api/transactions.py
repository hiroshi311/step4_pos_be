from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy.orm import Session
from typing import List
import datetime

from app.database.database import get_db
from app.models.transaction import Transaction
from app.models.transaction_detail import TransactionDetail
from app.models.product import Product
from app.schemas.transaction import TransactionCreate, TransactionResponse, TransactionDetailCreate

router = APIRouter()

@router.post("/purchase")
def create_purchase(transaction: TransactionCreate, db: Session = Depends(get_db)):
    total_amount_ex_tax = 0
    total_amount = 0
    transaction_details = []

    # 商品情報を先にすべて処理
    for idx, detail in enumerate(transaction.details, 1):
        product = db.query(Product).filter(Product.id == detail.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"商品ID {detail.product_id} が見つかりません")

        subtotal_ex_tax = float(product.price) * detail.quantity
        subtotal = subtotal_ex_tax * 1.1

        total_amount_ex_tax += subtotal_ex_tax
        total_amount += subtotal

        transaction_details.append({
            "product_id": product.id,
            "product_code": product.barcode,
            "product_name": product.name,
            "product_price": float(product.price),
            "tax_code": detail.tax_cd,
            "quantity": detail.quantity
        })


    # Transaction作成（flush前に合計を入れる）
    db_transaction = Transaction(
        employee_code=transaction.emp_cd,
        store_code=transaction.store_cd,
        pos_no=transaction.pos_no,
        datetime=datetime.datetime.now(),
        payment_method=transaction.payment_method,
        total_amount=round(total_amount),
        total_amount_ex_tax=round(total_amount_ex_tax),
    )
    db.add(db_transaction)
    db.flush()  # この時点で合計金額が入っているのでエラーにならない

    # 明細の追加
    for detail in transaction_details:
        db_detail = TransactionDetail(
            transaction_id=db_transaction.TRD_ID,
            **detail
        )
        db.add(db_detail)

    db.commit()
    db.refresh(db_transaction)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "購入完了",
            "totalAmt": int(total_amount),
            "totalAmtExTax": int(total_amount_ex_tax),
            "transactionId": db_transaction.TRD_ID
        }
    )


@router.get("/transactions", response_model=List[TransactionResponse])
def get_transactions(db: Session = Depends(get_db)):
    """取引履歴を取得するエンドポイント"""
    transactions = db.query(Transaction).order_by(Transaction.DATETIME.desc()).all()
    return transactions

@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """特定の取引の詳細を取得するエンドポイント"""
    transaction = db.query(Transaction).filter(Transaction.TRD_ID == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="取引が見つかりません")
    return transaction 