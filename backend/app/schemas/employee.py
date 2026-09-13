from pydantic import BaseModel, Field


class EmployeeRegister(BaseModel):
    jobNumber: str = Field(..., max_length=20)
    name: str = Field(..., max_length=50)
    password: str = Field(..., min_length=6)
    department: str = Field(..., description="INVESTMENT/FINANCE/OPERATION/CASHIER")
    rank: str = Field(..., description="员工 / 经理")