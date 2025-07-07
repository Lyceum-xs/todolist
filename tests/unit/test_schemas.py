import datetime as dt
import pytest
from pydantic import ValidationError
from src.app import schemas

# --- Task Schemas ---

@pytest.mark.parametrize("name", ["合法的任务名", "a"])
def test_task_create_valid(name):
    """测试：合法的任务创建数据应该能通过验证"""
    schemas.TaskCreate(name=name)

@pytest.mark.parametrize("name", ["", "  "])
def test_task_create_invalid_name(name):
    """测试：空的或只有空格的任务名应该无法通过验证"""
    with pytest.raises(ValidationError):
        schemas.TaskCreate(name=name)

def test_task_update_valid():
    """测试：合法的任务更新数据应该能通过验证"""
    payload = {
        "name": "新名字",
        "description": "新描述",
        "due_date": dt.datetime.now(),
        "completed": True
    }
    model = schemas.TaskUpdate(**payload)
    assert model.name == "新名字"
    assert model.completed is True

# --- Habit Schemas ---

def test_habit_create_valid():
    """测试：合法的习惯创建数据应该能通过验证"""
    schemas.HabitCreate(name="每天运动", duration=30)

@pytest.mark.parametrize("field, value", [
    ("name", ""),          # 名字不能为空
    ("duration", -1),      # 时长不能为负数
])
def test_habit_create_invalid(field, value):
    """测试：非法的习惯创建数据应该抛出 ValidationError"""
    payload = {"name": "合法名字", "duration": 10}
    payload[field] = value
    with pytest.raises(ValidationError):
        schemas.HabitCreate(**payload)

def test_habit_log_out_valid():
    """测试：合法的打卡日志输出模型"""
    schemas.HabitLogOut(id=1, habit_id=1, date=dt.date.today())