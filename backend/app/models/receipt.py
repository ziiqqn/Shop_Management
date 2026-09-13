from sqlalchemy import Column, BigInteger, Date, DECIMAL, Integer, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Receipt(Base):
    __tablename__ = "receipt"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tenant_id = Column(BigInteger, nullable=False)
    contract_id = Column(BigInteger, nullable=False)
    receipt_time = Column(Date, nullable=False)
    receivable_amount = Column(DECIMAL(12, 2), nullable=False)
    paid_amount = Column(DECIMAL(12, 2), default=0)
    reminder_sent = Column(Integer, default=0)
    create_time = Column(DateTime, server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "tenantId": self.tenant_id,
            "contractId": self.contract_id,
            "receiptTime": str(self.receipt_time),
            "receivableAmount": float(self.receivable_amount),
            "paidAmount": float(self.paid_amount),
            "unpaidAmount": float(self.receivable_amount - self.paid_amount),
            "reminderSent": self.reminder_sent,
        }