import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session,declarative_base
from contextlib import contextmanager
from typing import Generator

# 数据库配置
# 项目根目录 (todolist/)
BASE_DIR = Path(__file__).resolve().parent.parent
# 数据库文件路径，默认为项目根下 todo.db，可由环境变量覆盖
default_db = BASE_DIR / "todo.db"
default_db.parent.mkdir(parents=True, exist_ok=True)
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{default_db}")
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, future=True
)

# 会话工厂
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True)

# 线程安全的会话作用域
SessionScoped = scoped_session(SessionLocal)

#声明基类
Base = declarative_base()

def create_tables():
    from . import models  # 触发模型注册
    Base.metadata.create_all(bind=engine)

def drop_tables(): # 用于清空数据库
    Base.metadata.drop_all(bind=engine)

@contextmanager
def db_session() -> Generator[Session, None, None]:
    db = SessionLocal()  # 1. 创建会话
    try:
        yield db        # 2. 交出会话控制权
    except Exception:
        db.rollback()   # 3. 异常时回滚
        raise
    finally:
        db.close()      # 4. 确保关闭
