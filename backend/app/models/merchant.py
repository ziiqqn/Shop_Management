from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class MerchantAccount(Base):
    __tablename__ = "merchant_account"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tenant_id = Column(BigInteger, nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    create_time = Column(DateTime, server_default=func.now())