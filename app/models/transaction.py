from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP, CHAR
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.database import Base

class Transaction(Base):
    __tablename__ = "transaction"

    # PKとなる取引ID
    TRD_ID = Column("TRD_ID", Integer, primary_key=True, index=True)
    
    # 取引日時
    datetime = Column("datetime", TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    
    # レジ担当者コード（デフォルト：9999999999）
    employee_code = Column("emp_cd", CHAR(10), nullable=False, server_default='9999999999')
    
    # 店舗コード（固定値：'30'）
    store_code = Column("store_cd", CHAR(5), nullable=False, server_default='30')
    
    # POS機ID（固定値：'90'）
    pos_no = Column("pos_no", CHAR(3), nullable=False, server_default='90')
    
    # 合計金額（税込・税抜）
    total_amount = Column("TOTAL_AMT", Integer, nullable=False)
    total_amount_ex_tax = Column("TTL_AMT_EX_TAX", Integer, nullable=False)
    
    # 支払方法
    payment_method = Column(String(50), nullable=False)

    # タイムスタンプ（監査用）
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )

    # リレーションシップ
    details = relationship("TransactionDetail", back_populates="transaction") 