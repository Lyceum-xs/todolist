import pytest
from datetime import date, timedelta
from src.app.services import TaskService, HabitService
from src.app.models import Task, Habit, HabitLog

# --- 辅助函数 ---

def create_task(db_session, name, **kwargs):
    """在数据库中创建一个任务以供测试"""
    task = Task(name=name, **kwargs)
    db_session.add(task)
    db_session.commit()
    return task

def create_habit(db_session, name, **kwargs):
    """在数据库中创建一个习惯以供测试"""
    habit = Habit(name=name, **kwargs)
    db_session.add(habit)
    db_session.commit()
    return habit

# --- 测试 TaskService ---

def test_create_task_with_invalid_parent(db_session):
    """测试：创建任务时若父任务不存在，应抛出 ValueError"""
    with pytest.raises(ValueError, match="父任务ID 999 不存在"):
        TaskService.create_task(db_session, {"name": "新任务", "parent_id": 999})

def test_update_task_to_be_its_own_parent(db_session):
    """测试：更新任务时不能将自己设为父任务"""
    task = create_task(db_session, "一个任务")
    with pytest.raises(ValueError, match="不能将任务设置为自己的父任务"):
        TaskService.update_task(db_session, task.id, {"parent_id": task.id})

def test_get_non_existent_task_raises_error(db_session):
    """测试：获取或删除不存在的任务时应抛出 ValueError"""
    with pytest.raises(ValueError, match="任务不存在"):
        TaskService.get_task(db_session, 999)

    with pytest.raises(ValueError, match="任务不存在"):
        TaskService.delete_task(db_session, 999)

# --- 测试 HabitService ---

def test_create_habit_with_duplicate_name_raises_error(db_session):
    """测试：创建重名习惯应抛出 ValueError"""
    create_habit(db_session, "冥想")
    with pytest.raises(ValueError, match="习惯 '冥想' 已存在"):
        HabitService.create_habit(db_session, {"name": "冥想"})

def test_create_habit_log_for_non_existent_habit(db_session):
    """测试：为不存在的习惯打卡应抛出 ValueError"""
    with pytest.raises(ValueError, match="习惯不存在"):
        HabitService.create_habit_log(db_session, 999, {})

def test_create_duplicate_habit_log_raises_error(db_session):
    """测试：同一天重复为习惯打卡应抛出 ValueError"""
    habit = create_habit(db_session, "阅读")
    HabitService.create_habit_log(db_session, habit.id, {"date": date.today()})
    with pytest.raises(ValueError, match="今日已打卡，请勿重复操作"):
        HabitService.create_habit_log(db_session, habit.id, {"date": date.today()})

def test_habit_streak_logic(db_session):
    """测试：持续打卡天数的计算逻辑"""
    habit = create_habit(db_session, "健身")
    today = date.today()
    
    # 场景1: 没有打卡记录，天数为 0
    assert HabitService.get_habit_streak(db_session, habit.id) == 0

    # 场景2: 连续打卡3天（前天、昨天、今天）
    db_session.add_all([
        HabitLog(habit_id=habit.id, date=today - timedelta(days=2)),
        HabitLog(habit_id=habit.id, date=today - timedelta(days=1)),
        HabitLog(habit_id=habit.id, date=today),
    ])
    db_session.commit()
    assert HabitService.get_habit_streak(db_session, habit.id) == 3

    # 场景3: 中断了打卡（只有今天和前天）
    # 先清理之前的log
    db_session.query(HabitLog).delete()
    db_session.commit()
    db_session.add_all([
        HabitLog(habit_id=habit.id, date=today - timedelta(days=2)),
        HabitLog(habit_id=habit.id, date=today),
    ])
    db_session.commit()
    # 因为昨天断了，所以只从今天开始算，是1天
    assert HabitService.get_habit_streak(db_session, habit.id) == 1