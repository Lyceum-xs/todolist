"""
pytest tests/unit/test_services.py -q
"""
from datetime import datetime, timedelta, timezone

from src.app.services import TaskService, HabitService

#测试TaskService
def test_task_crud():
    #创建任务
    task_in = {
        "name": "读完《自制力》第一章",
        "description": "每日阅读任务",
        "priority": 2,
        "due_date": (datetime.now(timezone.utc) + timedelta(days=3)).isoformat()
    }
    task = TaskService.create_task(task_in)
    assert task.id > 0
    assert task.name == task_in["name"]

    #查询任务
    same = TaskService.get_task(task.id)
    assert same.id == task.id

    #更新任务
    updated = TaskService.update_task(task.id, {"priority": 1})
    assert updated.id == task.id

    #查询所有任务
    all_tasks = TaskService.get_all_tasks()
    assert any(t.id == task.id for t in all_tasks)

    #删除任务
    assert TaskService.delete_task(task.id) is True
    assert TaskService.get_task(task.id) is None


#测试HabitService
def test_habit_flow():
    #新建习惯
    habit = HabitService.create_habit({
        "name": "喝水",
        "description": "每日 8 杯水",
        "period": "daily"
    })
    assert habit.id > 0

    #修改习惯
    habit2 = HabitService.update_habit(habit.id, {"description": "每日 6 杯水"})
    assert habit2.description == "每日 6 杯水"

    #添加打卡记录
    log = HabitService.create_habit_log(habit.id, {"note": "Day1✅"})
    assert log.id > 0

    #查询打卡记录
    logs = HabitService.get_habit_logs(habit.id)
    assert len(logs) == 1

    #获取所有习惯
    all_habits = HabitService.get_all_habits()
    assert any(h.id == habit.id for h in all_habits)

    #删除习惯记录
    assert HabitService.delete_habit(habit.id) is True
    assert HabitService.get_habit(habit.id) is None
