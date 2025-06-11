from sqlalchemy import Column, Integer, String, CHAR, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base

class TransactionDetail(Base):
    __tablename__ = "transaction_detail"

    TRD_ID = Column(Integer, ForeignKey("transaction.TRD_ID"), nullable=False)
    DTL_ID = Column(Integer, primary_key=True, autoincrement=True)
    PRD_ID = Column(Integer, ForeignKey("product.id"), nullable=False)
    PRD_CODE = Column(CHAR(13), nullable=False)
    PRD_NAME = Column(String(50), nullable=False)
    PRD_PRICE = Column(Integer, nullable=False)
    TAX_CD = Column(CHAR(2), nullable=False, server_default='10')
    quantity = Column(Integer, nullable=False, default=1)

    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )

    # リレーション
    transaction = relationship("Transaction", back_populates="details")
    product = relationship("Product")
