import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session,declarative_base
from contextlib import contextmanager
from typing import Generator

# 获取当前文件的目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 设置数据库文件路径
DATABASE_PATH = os.path.join(BASE_DIR, 'todo.db')
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, future=True
)

# 创建数据库会话工厂
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True)

# 创建线程安全的会话
SessionScoped = scoped_session(SessionLocal)

# 定义数据库模型基类
Base = declarative_base()

def create_tables():
    from . import models  # 模型初始化
    print('Creating tables...')
    print(f"Database path: {DATABASE_PATH}")
    Base.metadata.create_all(bind=engine)
    print('Tables created successfully!')

def drop_tables(): # 删除所有数据库表
    Base.metadata.drop_all(bind=engine)

@contextmanager
def db_session() -> Generator[Session, None, None]:
    # 创建数据库会话
    db = SessionLocal()  
    try:
        # 提供数据库会话给调用的人
        yield db        
    except Exception:
        # 发生异常时滚回
        db.rollback()   
        raise
    finally:
        # 关闭数据库会话
        db.close()      

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
