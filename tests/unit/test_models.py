"""
pytest tests/unit/test_models.py -q
"""
from datetime import datetime, timedelta, timezone
import sqlalchemy as sa
import pytest

from src.app import models

# ---------- 通用 session fixture ----------
@pytest.fixture
def db_session():
    """从上一层 conftest 获取同一个 engine，再建独立 Session"""
    from conftest import engine   # 复用已创建的内存 engine
    Session = sa.orm.sessionmaker(bind=engine, expire_on_commit=False, future=True)
    with Session() as session:
        yield session
        session.rollback()  # 确保单个用例结束后干净


# ---------- Task ----------
def test_task_priority_and_subtasks(db_session):
    # 创建父子任务
    parent = models.Task(
        name="父任务",
        importance=True,
        urgent=False,
        due_date=datetime.now(timezone.utc) + timedelta(days=2)
    )
    child = models.Task(
        name="子任务",
        importance=False,
        urgent=True,
        due_date=datetime.now(timezone.utc) + timedelta(days=1),
        parent=parent
    )
    db_session.add(parent)
    db_session.commit()

    # 1) priority_parameter 计算
    parent_priority = parent.priority_parameter
    child_priority  = child.priority_parameter
    assert 0 <= parent_priority <= 1
    assert 0 <= child_priority  <= 1
    # 通常子任务更急 → 权重高
    assert child_priority > parent_priority

    # 2) 级联删除
    db_session.delete(parent)
    db_session.commit()

    # 此时数据库里不应再有 child
    remaining = db_session.query(models.Task).count()
    assert remaining == 0


# ---------- Habit & HabitLog ----------
def test_habit_and_logs_cascade(db_session):
    habit = models.Habit(name="喝水", description="每日 8 杯水")
    log1  = models.HabitLog(habit=habit)  # 自动关联
    db_session.add(habit)
    db_session.commit()

    # 1) 日志应在 relationship 中可见
    assert len(habit.logs) == 1

    # 2) 删 habit → log 级联删除
    db_session.delete(habit)
    db_session.commit()
    assert db_session.query(models.Habit).count() == 0
    assert db_session.query(models.HabitLog).count() == 0