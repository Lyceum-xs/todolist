import pytest
from httpx import AsyncClient

from src.app.main import app   

@pytest.mark.asyncio
async def test_health_returns_200_and_message():
    """
    GET /health 应返回 200 且包含 status 字段
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    # 根据你的实现调整断言 ↓↓↓
    assert data.get("status") == "ok"   # 根据实际实现调整

@pytest.mark.asyncio
async def test_create_and_get_task_flow(db_session, monkeypatch):
    """
    一个最小闭环：新增任务 → 列表中能查到
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {"title": "Pytest Task", "description": "demo"}
        resp = await ac.post("/tasks", json=payload)
        assert resp.status_code == 201
        task_id = resp.json()["id"]

        list_resp = await ac.get("/tasks")
        ids = [t["id"] for t in list_resp.json()]
        assert task_id in ids