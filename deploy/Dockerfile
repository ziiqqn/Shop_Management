# ============================================
# 商铺信息管理系统 - Docker 镜像
# 一个容器同时运行 FastAPI 后端 + Vue 前端
# ============================================

FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量（避免 Python 生成 .pyc，输出实时日志）
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Shanghai

# 安装系统依赖（pymysql 编译需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 先复制依赖清单，利用 Docker 层缓存
COPY backend/requirements.txt /app/backend/requirements.txt

# 安装 Python 依赖
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# 复制后端代码
COPY backend/ /app/backend/

# 复制前端代码（静态资源，被 FastAPI 挂载）
COPY frontend/ /app/frontend/

# 复制数据库脚本（首次启动可用）
COPY database/ /app/database/

# 工作目录切换到后端
WORKDIR /app/backend

# 暴露端口（Render 会自动读取）
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]