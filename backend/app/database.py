from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker,declarative_base
from app.config import settings

# 用 URL.create() 构造连接串，自动转义特殊字符
DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=settings.DB_USER,
    password=settings.DB_PASSWORD,   # 特殊字符会被自动处理
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME,
    query={"charset": "utf8mb4"},
)

# 创建引擎（echo=True 会打印 SQL，方便调试）
engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

# 创建会话工厂
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# 所有模型的基类
Base = declarative_base()

def get_db():
    """依赖注入：每个请求一个数据库会话，用完自动关闭"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()