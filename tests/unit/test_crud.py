import pytest
from pydantic import ValidationError

from src.app import crud, models, schemas

@pytest.fixture(scope="module")
def sample_task():
    """
    提供一个合法的用于创建任务的 schema。
    修正: 根据 Pydantic 模型的要求，将字段 'title' 修改为 'name'。
    """
    return schemas.TaskCreate(name="一个示例任务", description="任务描述")

def test_create_task_increases_count(db_session, sample_task):
    """测试创建任务后，数据库中的任务总数会增加。"""
    before_count = len(crud.get_tasks_by_status(db_session, status="all"))
    crud.create_task(db_session, sample_task)
    after_count = len(crud.get_tasks_by_status(db_session, status="all"))
    assert after_count == before_count + 1


@pytest.mark.parametrize(
    "name, is_valid",
    [
        ("一个合法的任务名", True),
        ("", False),  # 任务名不应为空字符串
    ],
)
def test_name_validation(name, is_valid):
    """
    测试 TaskCreate 模型中 'name' 字段的校验逻辑。
    修正: 实现了这个测试，以真正执行校验检查。
    """
    if is_valid:
        # 对于合法的输入，不应该抛出任何异常
        schemas.TaskCreate(name=name)
    else:
        # 对于非法的输入，应该抛出 ValidationError
        with pytest.raises(ValidationError):
            schemas.TaskCreate(name=name)

def test_get_tasks_by_status(db_session):
    """测试根据不同状态筛选任务"""
    crud.create_task(db_session, schemas.TaskCreate(name="已完成的任务", completed=True))
    crud.create_task(db_session, schemas.TaskCreate(name="待办任务", completed=False))

    completed_tasks = crud.get_tasks_by_status(db_session, status="completed")
    assert len(completed_tasks) == 1
    assert completed_tasks[0].name == "已完成的任务"

    pending_tasks = crud.get_tasks_by_status(db_session, status="pending")
    assert len(pending_tasks) == 1
    assert pending_tasks[0].name == "待办任务"

    all_tasks = crud.get_tasks_by_status(db_session, status="all")
    assert len(all_tasks) == 2