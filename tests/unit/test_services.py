"""
pytest tests/unit/test_services.py -q
"""
from datetime import datetime, timedelta

from src.app.services import TaskService, HabitService

# ---------- TaskService ----------
def test_task_crud():
    # 创建
    task_in = {
        "name": "读完《自制力》第一章",
        "description": "每日阅读任务",
        "priority": 2,
        "due_date": (datetime.utcnow() + timedelta(days=3)).isoformat()
    }
    task = TaskService.create_task(task_in)
    assert task.id > 0
    assert task.name == task_in["name"]

    # 查询单条
    same = TaskService.get_task(task.id)
    assert same.id == task.id

    # 更新
    updated = TaskService.update_task(task.id, {"priority": 1})
    assert updated.id == task.id

    # get_all
    all_tasks = TaskService.get_all_tasks()
    assert any(t.id == task.id for t in all_tasks)

    # 删除
    assert TaskService.delete_task(task.id) is True
    assert TaskService.get_task(task.id) is None


# ---------- HabitService ----------
def test_habit_flow():
    # 创建习惯
    habit = HabitService.create_habit({
        "name": "喝水",
        "description": "每日 8 杯水",
        "period": "daily"
    })
    assert habit.id > 0

    # 更新习惯
    habit2 = HabitService.update_habit(habit.id, {"description": "每日 6 杯水"})
    assert habit2.description == "每日 6 杯水"

    # 写一条打卡
    log = HabitService.create_habit_log(habit.id, {"note": "Day1✅"})
    assert log.id > 0

    # 读取打卡
    logs = HabitService.get_habit_logs(habit.id)
    assert len(logs) == 1

    # 查看全部习惯
    all_habits = HabitService.get_all_habits()
    assert any(h.id == habit.id for h in all_habits)

    # 删除习惯
    assert HabitService.delete_habit(habit.id) is True
    assert HabitService.get_habit(habit.id) is None