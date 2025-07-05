import pytest

from src.app import crud, models, schemas

@pytest.fixture(scope="module")
def sample_task():
    return schemas.TaskCreate(title="Sample", description="demo")

def test_create_task_increases_count(db_session, sample_task):
    """创建任务后，数据库条目 +1"""
    before = crud.task_count(db_session)
    crud.create_task(db_session, sample_task)
    after = crud.task_count(db_session)
    assert after == before + 1

@pytest.mark.parametrize(
    "title, expected",
    [
        ("Hello", True),
        ("", False),
    ],
)
def test_title_validation(title, expected):
    """标题不能为空"""
    # TODO: 用 pydantic/自定义校验验证 title
    pass