from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.database import get_db
from app.models.product import Product
from app.schemas.product import ProductResponse

router = APIRouter()

@router.get("/products", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    """商品一覧を取得するエンドポイント"""
    products = db.query(Product).all()
    return products

@router.get("/product", response_model=Optional[ProductResponse])
def get_product_by_code(code: str, db: Session = Depends(get_db)):
    print(f"受け取ったcode: '{code}' (長さ: {len(code)})")
    code = code.strip()  # ← ここを追加
    product = db.query(Product).filter(Product.barcode == code).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品が見つかりません")
    return product

@router.get("/products/barcode/{barcode}", response_model=ProductResponse)
def get_product_by_barcode(barcode: str, db: Session = Depends(get_db)):
    """バーコードで商品を検索するエンドポイント（レガシー）"""
    product = db.query(Product).filter(Product.barcode == barcode).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品が見つかりません")
    return product 