import datetime as _dt
import pytest
from pydantic import ValidationError
from src.app import schemas


# ---------- TaskUpdate ----------
@pytest.mark.parametrize(
    "payload",
    [
        {"title": "new title"},
        {"description": "updated"},
        {"due_date": _dt.date.today() + _dt.timedelta(days=1)},
        {"completed": True},
    ],
)
def test_task_update_valid(payload):
    model = schemas.TaskUpdate(**payload)
    for k, v in payload.items():
        assert getattr(model, k) == v


@pytest.mark.parametrize(
    "field,value",
    [
        ("title", ""),                        # 不能为空
        ("due_date", "invalid-date"),         # 格式错误
    ],
)
def test_task_update_invalid(field, value):
    base = {"title": "tmp"}  # 至少给一个合法字段
    base[field] = value
    with pytest.raises(ValidationError):
        schemas.TaskUpdate(**base)


# ---------- HabitCreate ----------
def test_habit_create_valid():
    model = schemas.HabitCreate(name="Drink Water", goal_per_day=8)
    assert model.name == "Drink Water"
    assert model.goal_per_day == 8


@pytest.mark.parametrize(
    "field,value",
    [
        ("name", ""),
        ("goal_per_day", 0),
    ],
)
def test_habit_create_invalid(field, value):
    kwargs = {"name": "tmp", "goal_per_day": 1}
    kwargs[field] = value
    with pytest.raises(ValidationError):
        schemas.HabitCreate(**kwargs)


# ---------- HabitLog ----------
def test_habit_log_valid():
    model = schemas.HabitLog(habit_id=1, count=3, date=_dt.date.today())
    assert model.count == 3


@pytest.mark.parametrize("count", [-1, 0])
def test_habit_log_invalid_count(count):
    with pytest.raises(ValidationError):
        schemas.HabitLog(habit_id=1, count=count, date=_dt.date.today())