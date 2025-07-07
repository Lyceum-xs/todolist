from datetime import datetime, timedelta, timezone
import pytest
from src.app import models

def test_task_priority_calculation(db_session):
    """测试：任务优先级的计算逻辑"""
    # 场景1：紧急且重要
    task1 = models.Task(
        name="紧急且重要",
        importance=True,
        urgent=True,
        due_date=datetime.now(timezone.utc) + timedelta(days=1)
    )
    # 场景2：不紧急不重要
    task2 = models.Task(name="不紧急不重要", importance=False, urgent=False)
    
    db_session.add_all([task1, task2])
    db_session.commit()

    # 修正: 最低优先级可以是 0，所以使用 <=
    assert 0 <= task2.priority_parameter < task1.priority_parameter <= 1

def test_task_cascade_delete(db_session):
    """测试：删除父任务时，其子任务也应被级联删除"""
    parent = models.Task(name="父任务")
    child = models.Task(name="子任务", parent=parent)
    
    db_session.add(parent)
    db_session.commit()
    
    parent_id = parent.id
    child_id = child.id
    
    # 确认父子任务都已在数据库中
    assert db_session.get(models.Task, parent_id) is not None
    assert db_session.get(models.Task, child_id) is not None

    # 删除父任务
    db_session.delete(parent)
    db_session.commit()

    # 确认父子任务都已被删除
    assert db_session.get(models.Task, parent_id) is None
    assert db_session.get(models.Task, child_id) is None