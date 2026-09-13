from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """登录请求体"""
    username: str = Field(..., description="工号 / 用户名")
    password: str = Field(..., description="密码")


class RegisterRequest(BaseModel):
    """商户注册请求体"""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    tenantName: str = Field(..., description="租户名称")
    idCard: str = Field(..., min_length=18, max_length=18, description="18位身份证")
    brandType: str = Field(..., description="连锁 / 个体")
    brandName: str = Field(..., description="品牌名")


class LoginResponse(BaseModel):
    """登录响应"""
    token: str
    role: str
    username: str