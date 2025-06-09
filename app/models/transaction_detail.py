from sqlalchemy import Column, Integer, String, CHAR, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.database import Base

class TransactionDetail(Base):
    __tablename__ = "transaction_detail"

    # 主キーと外部キー
    transaction_id = Column("TRD_ID", Integer, ForeignKey("transaction.TRD_ID"), nullable=False)
    detail_id = Column("DTL_ID", Integer, primary_key=True, autoincrement=True)
    product_id = Column("PRD_ID", Integer, ForeignKey("product.id"), nullable=False)
    
    # 商品情報
    product_code = Column("PRD_CODE", CHAR(13), nullable=False)
    product_name = Column("PRD_NAME", String(50), nullable=False)
    product_price = Column("PRD_PRICE", Integer, nullable=False)
    
    # 税コード（固定値：'10'）
    tax_code = Column("TAX_CD", CHAR(2), nullable=False, server_default='10')

    # 数量
    quantity = Column(Integer, nullable=False, default=1)

    # タイムスタンプ（監査用）
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )

    # リレーションシップ
    transaction = relationship("Transaction", back_populates="details")
    product = relationship("Product") 