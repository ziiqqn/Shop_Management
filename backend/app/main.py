from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers import auth, shop, tenant, contract, rent, receipt, bill, employee
from app.scheduler.monthly_receipt import start_scheduler, shutdown_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    shutdown_scheduler()


app = FastAPI(title="商铺信息管理系统 API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== 1. 先注册所有 API 路由 =====
app.include_router(auth.router)
app.include_router(shop.router)
app.include_router(tenant.router)
app.include_router(contract.router)
app.include_router(rent.router)
app.include_router(receipt.router)
app.include_router(bill.router)
app.include_router(employee.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}


# ===== 2. 最后挂载前端静态资源 =====
# 项目根目录下的 frontend/
BASE_DIR = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
else:
    @app.get("/")
    def root():
        return {"message": "前端目录未找到，请检查 frontend/ 是否存在"}