import pytest
from fastapi.testclient import TestClient

# --- 辅助函数 ---
def create_task_helper(client: TestClient, name: str, parent_id: int | None = None) -> dict:
    """辅助函数：创建一个任务并返回其 JSON 数据"""
    payload = {"name": name, "importance": False, "urgent": False}
    if parent_id:
        payload["parent_id"] = parent_id
    response = client.post("/tasks/", json=payload)
    assert response.status_code == 201, f"创建任务失败: {response.text}"
    return response.json()

def create_habit_helper(client: TestClient, name: str) -> dict:
    """辅助函数：创建一个习惯并返回其 JSON 数据"""
    payload = {"name": name, "description": f"描述 {name}"}
    response = client.post("/habits/", json=payload)
    assert response.status_code == 201, f"创建习惯失败: {response.text}"
    return response.json()


# --- 测试任务(Tasks)相关的 API ---

def test_get_task_not_found(client: TestClient):
    """测试：获取一个不存在的任务应该返回 404"""
    response = client.get("/tasks/9999")
    assert response.status_code == 404

def test_create_task_with_invalid_name(client: TestClient):
    """测试使用空名称创建任务会失败"""
    response = client.post("/tasks/", json={"name": ""})
    assert response.status_code == 422 # 检查是否返回“不可处理的实体”错误

def test_task_lifecycle(client: TestClient):
    """测试：任务的完整生命周期（创建 -> 获取 -> 列表 -> 更新 -> 搜索 -> 删除）"""
    task_data = create_task_helper(client, "学习 FastAPI")
    task_id = task_data["id"]
    
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "学习 FastAPI"

    update_payload = {"completed": True, "name": "完成 FastAPI 学习"}
    response = client.patch(f"/tasks/{task_id}", json=update_payload)
    assert response.status_code == 200
    assert response.json()["completed"] is True

    response = client.get("/tasks?status=completed")
    assert any(t["id"] == task_id for t in response.json())

    response = client.get("/tasks/search?q=FastAPI")
    assert response.status_code == 200
    assert any(t["id"] == task_id for t in response.json())

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404

def test_task_parent_child_relationship(client: TestClient):
    """测试：任务的父子关系"""
    parent_task = create_task_helper(client, "父任务")
    parent_id = parent_task["id"]
    create_task_helper(client, "子任务1", parent_id=parent_id)
    response = client.get(f"/tasks/{parent_id}/children")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_search_task_no_results(client: TestClient):
    """测试搜索一个不存在的任务"""
    create_task_helper(client, "一个真实存在的任务")
    response = client.get("/tasks/search?q=一个不存在的关键词")
    assert response.status_code == 200
    assert len(response.json()) == 0
# --- 测试习惯(Habits)相关的 API ---

def test_habit_lifecycle_and_logs(client: TestClient):
    """测试：习惯的完整生命周期和打卡记录"""
    habit_data = create_habit_helper(client, "每天喝水")
    habit_id = habit_data["id"]

    log_response = client.post(f"/habits/{habit_id}/logs", json={})
    assert log_response.status_code == 201

    log_response_again = client.post(f"/habits/{habit_id}/logs", json={})
    assert log_response_again.status_code == 409

    logs_response = client.get(f"/habits/{habit_id}/logs")
    assert len(logs_response.json()) == 1

    streak_response = client.get(f"/habits/{habit_id}/streak")
    assert streak_response.status_code == 200
    assert streak_response.json() == 1

    delete_response = client.delete(f"/habits/{habit_id}")
    assert delete_response.status_code == 204

def test_update_non_existent_task(client: TestClient):
    """测试更新一个不存在的任务会返回 404"""
    response = client.patch("/tasks/99999", json={"completed": True})
    assert response.status_code == 404

def test_get_logs_for_non_existent_habit(client: TestClient):
    """测试获取一个不存在的习惯的打卡记录会返回 404"""
    response = client.get("/habits/99999/logs")
    assert response.status_code == 404