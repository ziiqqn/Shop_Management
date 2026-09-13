from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, shop, tenant, contract, rent, receipt, bill, employee
from app.scheduler.monthly_receipt import start_scheduler, shutdown_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    shutdown_scheduler()


app = FastAPI(
    title="商铺信息管理系统 API",
    version="1.0.0",
    lifespan=lifespan
)

# 前后端分离，必须开放 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://impartial-tenderness-production-5c31.up.railway.app",
                   "http://localhost:5500",
                   "http://127.0.0.1:5500"
    ],       # 生产环境可换成具体前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册所有业务路由
app.include_router(auth.router)
app.include_router(shop.router)
app.include_router(tenant.router)
app.include_router(contract.router)
app.include_router(rent.router)
app.include_router(receipt.router)
app.include_router(bill.router)
app.include_router(employee.router)


@app.get("/")
def root():
    """后端根路径，仅用于健康检查"""
    return {"message": "商铺信息管理系统 API 运行中", "docs": "/docs"}


@app.get("/api/health")
def health():
    return {"status": "ok"}