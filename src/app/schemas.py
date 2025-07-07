from datetime import datetime, date
from pydantic import BaseModel, Field, ConfigDict, field_serializer, constr

# --- 任务(Task)相关的 Schema ---

class TaskBase(BaseModel):
    """任务的基础模型，包含创建和读取时共有的字段"""
    name: constr(strip_whitespace=True, min_length=1, max_length=255) = Field(description="任务名称")
    description: str | None = Field(None, description="任务的详细描述")
    due_date: datetime | None = Field(None, description="任务截止日期")
    importance: bool = Field(False, description="是否为重要任务")
    urgent: bool = Field(False, description="是否为紧急任务")
    parent_id: int | None = Field(None, description="父任务的ID")
    completed: bool = Field(False, description="任务是否已完成")

    model_config = ConfigDict(title="任务基础信息")

class TaskCreate(TaskBase):
    """用于创建任务的模型"""
    model_config = ConfigDict(title="任务创建")

class TaskUpdate(BaseModel):
    """用于更新任务的模型，所有字段都是可选的"""
    name: constr(strip_whitespace=True, min_length=1, max_length=255) | None = Field(None, description="新的任务名称")
    description: str | None = Field(None, description="新的任务描述")
    due_date: datetime | None = Field(None, description="新的截止日期")
    completed: bool | None = Field(None, description="是否已完成")
    importance: bool | None = Field(None, description="新的重要性设置")
    urgent: bool | None = Field(None, description="新的紧急性设置")
    parent_id: int | None = Field(None, description="新的父任务ID")

    model_config = ConfigDict(title="任务更新")

class TaskOut(TaskBase):
    """用于从接口返回任务详情的模型"""
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime

    # 这个序列化器保留了您的自定义逻辑：在返回给前端时，将 None 值的 parent_id 转换为 0
    # 这有助于前端统一处理，避免对 null 值的额外判断
    @field_serializer('parent_id')
    def serialize_parent_id(self, parent_id: int | None, _info):
        """当从数据库取出的 parent_id 是 None 时，在接口返回中将其转换为 0"""
        return 0 if parent_id is None else parent_id

    model_config = ConfigDict(from_attributes=True, title="任务详情")


# --- 习惯(Habit)相关的 Schema ---

class HabitBase(BaseModel):
    """习惯的基础模型"""
    name: str = Field(..., min_length=1, max_length=128, description="习惯名称")
    description: str | None = Field(None, description="习惯的详细描述")
    # 设定默认值为0，并确保时长不能为负数
    duration: int = Field(0, ge=0, description="完成一次习惯所需的时间（分钟）")

    model_config = ConfigDict(title="习惯基础信息")

class HabitCreate(HabitBase):
    """用于创建习惯的模型"""
    model_config = ConfigDict(title="习惯创建")

class HabitUpdate(BaseModel):
    """用于更新习惯的模型，所有字段都是可选的，结构与 TaskUpdate 保持一致"""
    name: str | None = Field(None, min_length=1, max_length=128, description="新的习惯名称")
    description: str | None = Field(None, description="新的习惯描述")
    completed: bool | None = Field(None, description="今日是否已完成")
    duration: int | None = Field(None, ge=0, description="新的习惯时长")

    model_config = ConfigDict(title="习惯更新")

class HabitLogCreate(BaseModel):
    """用于创建打卡记录的模型"""
    # 如果不提供日期，则自动使用当前时间作为默认值
    date: datetime = Field(default_factory=datetime.now, description="打卡日期")

class HabitLogOut(BaseModel):
    """用于返回打卡记录详情的模型"""
    id: int
    habit_id: int
    date: date

    model_config = ConfigDict(from_attributes=True, title="打卡日志详情")

class HabitOut(HabitBase):
    """用于从接口返回习惯详情（包含打卡记录）的模型"""
    id: int
    logs: list[HabitLogOut] = []

    model_config = ConfigDict(from_attributes=True, title="习惯详情")