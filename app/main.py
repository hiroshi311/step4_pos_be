from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.products import router as products_router
from app.api.transactions import router as transactions_router
from app.database.database import engine
from app.models import product, transaction, transaction_detail

app = FastAPI(title="POS System API")

# データベーステーブルの作成
product.Product.__table__.create(bind=engine, checkfirst=True)
transaction.Transaction.__table__.create(bind=engine, checkfirst=True)
transaction_detail.TransactionDetail.__table__.create(bind=engine, checkfirst=True)

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 本番環境では適切に制限する必要があります
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの登録
app.include_router(products_router, prefix="/api", tags=["products"])
app.include_router(transactions_router, prefix="/api", tags=["transactions"])

# ルートエンドポイント
@app.get("/")
async def root():
    return {"message": "POS System API"} 