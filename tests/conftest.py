"""
全局测试夹具：
- 用 SQLite 内存库创建一次所有表，测试结束后销毁
- monkeypatch 替换 services.db_session -> 专用 TestingSessionLocal
"""
import pytest, sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# === 你的项目导入 ===
from src.app import models                      # Base & ORM 模型
from src.app import services                    # 要替换 db_session 的模块

# ---- 内存数据库 & 会话工厂 ----
TEST_DB_URL = "sqlite+pysqlite:///:memory:"
engine = sa.create_engine(TEST_DB_URL, future=True, echo=False)
TestingSessionLocal = sessionmaker(bind=engine, expire_on_commit=False, future=True)

# ---- 创建 / 销毁表 ----
@pytest.fixture(scope="session", autouse=True)
def _create_all():
    models.Base.metadata.create_all(bind=engine)
    yield
    models.Base.metadata.drop_all(bind=engine)

# ---- monkeypatch services.db_session ----
@pytest.fixture(autouse=True)
def _patch_db_session(monkeypatch):
    @contextmanager
    def _override():
        with TestingSessionLocal() as db:
            yield db
    monkeypatch.setattr(services, "db_session", _override)
    yield