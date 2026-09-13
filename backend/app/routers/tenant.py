from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate, TenantUpdate
from app.utils.deps import require_role
from app.constants import ROLE_INVESTMENT

router = APIRouter(prefix="/api/tenant", tags=["租户"])


@router.get("/list", summary="租户列表")
def list_tenants(db: Session = Depends(get_db),
                 user=Depends(require_role(ROLE_INVESTMENT))):
    return [t.to_dict() for t in db.query(Tenant).all()]


@router.get("/{tenant_id}", summary="租户详情")
def get_tenant(tenant_id: int, db: Session = Depends(get_db),
               user=Depends(require_role(ROLE_INVESTMENT))):
    t = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not t:
        raise HTTPException(404, "租户不存在")
    return t.to_dict()


@router.post("/add", summary="新增租户")
def add_tenant(data: TenantCreate, db: Session = Depends(get_db),
               user=Depends(require_role(ROLE_INVESTMENT))):
    tenant = Tenant(
        name=data.name,
        id_card=data.idCard,
        brand_type=data.brandType,
        brand_name=data.brandName
    )
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return {"message": "新增成功", "id": tenant.id}


@router.put("/update", summary="更新租户")
def update_tenant(data: TenantUpdate, db: Session = Depends(get_db),
                  user=Depends(require_role(ROLE_INVESTMENT))):
    tenant = db.query(Tenant).filter(Tenant.id == data.id).first()
    if not tenant:
        raise HTTPException(404, "租户不存在")
    tenant.name = data.name
    tenant.id_card = data.idCard
    tenant.brand_type = data.brandType
    tenant.brand_name = data.brandName
    db.commit()
    return {"message": "更新成功"}


@router.delete("/{tenant_id}", summary="删除租户")
def delete_tenant(tenant_id: int, db: Session = Depends(get_db),
                  user=Depends(require_role(ROLE_INVESTMENT))):
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(404, "租户不存在")
    db.delete(tenant)
    db.commit()
    return {"message": "删除成功"}