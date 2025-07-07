import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from src.app.main import app
from src.app.db import create_tables, drop_tables, SessionLocal, engine, Base
from src.app.models import Base
from sqlalchemy import create_engine, event

@pytest.fixture(scope="session")
def client():
    """
    提供一个在整个测试会话期间共享的 TestClient 实例。
    """
    # 在所有测试开始前，清理并创建一次表结构
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    # 所有测试结束后，再次清理
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    为每个测试函数提供一个独立的数据库会话。
    并在测试结束后，清空所有表的数据，确保测试的完全隔离。
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        # 回滚任何未提交的更改（以防万一）
        session.rollback()
        
        # 按外键依赖的反向顺序，清空所有表中的数据
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())
        
        # 提交清空操作
        session.commit()
        
        # 关闭会话
        session.close()