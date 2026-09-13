from sqlalchemy import Column, BigInteger, Date, DECIMAL, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Bill(Base):
    __tablename__ = "bill"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tenant_id = Column(BigInteger, nullable=False)
    receipt_id = Column(BigInteger, nullable=False)
    receivable_amount = Column(DECIMAL(12, 2), nullable=False)
    paid_amount = Column(DECIMAL(12, 2), default=0)
    payment_channel = Column(String(20))
    bill_month = Column(Date, nullable=False)
    is_paid = Column(Integer, default=0)
    create_time = Column(DateTime, server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "tenantId": self.tenant_id,
            "receiptId": self.receipt_id,
            "receivableAmount": float(self.receivable_amount),
            "paidAmount": float(self.paid_amount),
            "unpaidAmount": float(self.receivable_amount - self.paid_amount),
            "paymentChannel": self.payment_channel,
            "billMonth": str(self.bill_month),
            "isPaid": self.is_paid,
        }