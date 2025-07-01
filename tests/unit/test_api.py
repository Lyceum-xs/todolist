import pytest
from fastapi.testclient import TestClient
from src.app.main import app
from src.app.db import create_tables, engine

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    # 每个测试模块运行前重建表
    from src.app.models import Base
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_task_crud_and_subtree():
    # 1) 创建父任务
    r = client.post("/tasks/", json={"name":"T","importance":False,"urgent":False})
    assert r.status_code == 201
    tid = r.json()["id"]

    # 2) 子任务
    client.post("/tasks/", json={"name":"C1","importance":False,"urgent":False,"parent_id":tid})
    client.post("/tasks/", json={"name":"C2","importance":False,"urgent":False,"parent_id":tid})

    # 3) children_count
    r = client.get(f"/tasks/{tid}/children_count")
    assert r.status_code == 200 and r.json() == 2

    # 4) subtree (BFS)
    r = client.get(f"/tasks/{tid}/subtree?mode=bfs")
    body = r.json()
    assert r.status_code == 200 and {t["id"] for t in body} == {tid, body[1]["id"], body[2]["id"]}

def test_habit_and_logs():
    # 1) 创建一个习惯
    r = client.post(
        "/habits/",
        json={"name": "H1", "description": "测试习惯", "duration": 1},
    )
    assert r.status_code == 201
    hid = r.json()["id"]

    # 2) 为该习惯创建一次打卡记录
    r2 = client.post(
        f"/habits/{hid}/logs",
        json={},  # 日志只需 habit_id，其他由后端处理
    )
    assert r2.status_code == 201
    log = r2.json()
    assert log["habit_id"] == hid
    assert "date" in log

    # 3) 列出该习惯的所有打卡日志
    r3 = client.get(f"/habits/{hid}/logs")
    assert r3.status_code == 200
    logs = r3.json()
    assert isinstance(logs, list)
    assert len(logs) == 1
    assert logs[0]["id"] == log["id"]

def test_pomodoro_flow():
    r = client.post("/pomodoros/", json={})
    assert r.status_code == 201
    sid = r.json()["id"]
    r2 = client.patch(f"/pomodoros/{sid}/stop")
    assert r2.status_code == 200 and r2.json()["completed"] is True
    r3 = client.get("/pomodoros/")
    assert any(p["id"] == sid for p in r3.json())