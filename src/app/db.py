import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session,declarative_base
from contextlib import contextmanager
from typing import Generator

# 获取当前文件所在目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 数据库文件路径
DATABASE_PATH = os.path.join(BASE_DIR, 'todo.db')
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

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
    print('creating')
    print(f"Database path: {DATABASE_PATH}")  # 添加这行
    Base.metadata.create_all(bind=engine)
    print('created successfully')

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
