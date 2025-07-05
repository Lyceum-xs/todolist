import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.app.main import app, get_db
from src.app import models, crud
from src.app.db import Base

# ---------- 使用内存数据库 ----------
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


# ---------- 依赖覆盖 ----------
def _override_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = _override_db


@pytest.mark.asyncio
async def test_create_and_get_task():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # 创建
        resp = await ac.post(
            "/tasks",
            json={"title": "Write tests", "description": "coverage", "due_date": "2030-01-01"},
        )
        assert resp.status_code == 201
        data = resp.json()
        task_id = data["id"]

        # 获取
        resp = await ac.get(f"/tasks/{task_id}")
        assert resp.status_code == 200
        assert resp.json()["title"] == "Write tests"


@pytest.mark.asyncio
async def test_task_not_found():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/tasks/99999")
        assert resp.status_code == 404


@pytest.mark.asyncio
async def test_habit_create_validate_goal():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/habits", json={"name": "Run", "goal_per_day": 0})
        assert resp.status_code == 422  # 数据校验失败