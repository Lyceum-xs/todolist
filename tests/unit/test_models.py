from datetime import datetime, timedelta, timezone
import sqlalchemy as sa
import pytest

from src.app import models

#通用数据库会话
@pytest.fixture
def db_session():
    """使用共享的 engine，创建独立的会话"""
    from conftest import engine   #使用已存在的内存数据库 engine
    Session = sa.orm.sessionmaker(bind=engine, expire_on_commit=False, future=True)
    with Session() as session:
        yield session
        session.rollback()  #回滚以清理数据


#测试 Task
def test_task_priority_and_subtasks(db_session):
    #创建父任务和子任务
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

    #检查优先级参数
    parent_priority = parent.priority_parameter
    child_priority  = child.priority_parameter
    assert 0 <= parent_priority <= 1
    assert 0 <= child_priority  <= 1
    #子任务的优先级应高于父任务
    assert child_priority > parent_priority

    #测试级联删除
    db_session.delete(parent)
    db_session.commit()

    #数据库中不应剩下子任务
    remaining = db_session.query(models.Task).count()
    assert remaining == 0


#测试 Habit和HabitLog
def test_habit_and_logs_cascade(db_session):
    habit = models.Habit(name="喝水", description="每日 8 杯水")
    log1  = models.HabitLog(habit=habit)  #自动与Habit建立关联
    db_session.add(habit)
    db_session.commit()

    #检查日志是否添加成功
    assert len(habit.logs) == 1

    #删除Habit后应级联删除日志
    db_session.delete(habit)
    db_session.commit()
    assert db_session.query(models.Habit).count() == 0
    assert db_session.query(models.HabitLog).count() == 0