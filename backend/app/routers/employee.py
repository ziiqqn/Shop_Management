from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.employee import Employee
from app.schemas.employee import EmployeeRegister
from app.utils.security import hash_password
from app.utils.deps import require_role
from app.constants import ROLE_BOSS

router = APIRouter(prefix="/api/employee", tags=["员工"])


@router.post("/register", summary="老板注册新员工")
def register_employee(data: EmployeeRegister, db: Session = Depends(get_db),
                      user=Depends(require_role(ROLE_BOSS))):
    # 检查工号唯一
    if db.query(Employee).filter(Employee.job_number == data.jobNumber).first():
        raise HTTPException(400, "工号已存在")

    emp = Employee(
        name=data.name,
        job_number=data.jobNumber,
        department=data.department,
        rank=data.rank,
        password=hash_password(data.password)
    )
    db.add(emp)
    db.commit()
    return {"message": "注册成功", "id": emp.id}