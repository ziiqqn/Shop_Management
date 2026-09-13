from sqlalchemy import Column, BigInteger, String, Date, Integer, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Contract(Base):
    __tablename__ = "contract"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    contract_no = Column(String(50), unique=True, nullable=False)
    shop_id = Column(BigInteger, nullable=False)
    tenant_id = Column(BigInteger, nullable=False)
    pic_url = Column(String(200))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    audit_status = Column(Integer, default=0)
    audit_remark = Column(String(255))
    create_time = Column(DateTime, server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "contractNo": self.contract_no,
            "shopId": self.shop_id,
            "tenantId": self.tenant_id,
            "picUrl": self.pic_url,
            "startDate": str(self.start_date),
            "endDate": str(self.end_date),
            "auditStatus": self.audit_status,
            "auditRemark": self.audit_remark,
        }