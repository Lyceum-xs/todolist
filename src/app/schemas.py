from datetime import datetime
from pydantic import BaseModel, Field , ConfigDict, field_serializer
from typing_extensions import Annotated

class TaskBase(BaseModel):
    name: str = Field(..., max_length=255) #...表示创建必需
    description: str | None = None
    due_date: datetime | None = None
    importance: bool = False
    urgent: bool = False
    parent_id: int | None = None

    model_config = ConfigDict(title= "任务基础信息")

class TaskCreate(TaskBase):
    model_config = ConfigDict(title= "任务创建")

class TaskUpdate(BaseModel):
    name: str | None = Field(None, max_length=255)
    description: str | None = None
    due_date: datetime | None = None
    completed: bool | None = False
    importance: bool | None = False
    urgent: bool | None = False
    parent_id: int | None = None

    model_config = ConfigDict(title= "任务更新")

    @field_serializer('parent_id')
    def serialize_parent_id(self, parent_id: int | None, _info):
        """当从数据库取出的 parent_id 是 None 时，在接口返回中将其转换为 0"""
        return 0 if parent_id is None else parent_id

class TaskOut(TaskBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, title= "任务详情")

class HabitBase(BaseModel):
    name: str = Field(..., max_length=128)
    description: str | None = None
    duration: int| None = 0

    model_config = ConfigDict(title= "习惯基础信息")

class HabitCreate(HabitBase):
    model_config = ConfigDict(title= "习惯创建")

class HabitUpdate(HabitBase):
    name: str | None = Field(None, max_length=128)
    description: str | None = None
    completed: bool | None = False
    duration: int | None = None

    model_config = ConfigDict(title= "习惯更新")

class HabitLogCreate(BaseModel):
    date: datetime | None = None

class HabitLogOut(BaseModel):
    id: int
    habit_id: int
    date: datetime

    model_config = ConfigDict(from_attributes=True, title= "打卡日志详情")

class HabitOut(HabitBase):
    id: int
    logs: list[HabitLogOut] = []

    model_config = ConfigDict(from_attributes=True, title= "习惯详情")
