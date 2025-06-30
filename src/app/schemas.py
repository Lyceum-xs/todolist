from datetime import datetime
from pydantic import BaseModel, Field , ConfigDict
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

    model_config = ConfigDict(title= "任务更新")

class TaskOut(TaskBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, title= "任务详情")

class HabitBase(BaseModel):
    name: str = Field(..., max_length=128)
    description: str | None = None
    duration: int = 0

    model_config = ConfigDict(title= "习惯基础信息")

class HabitCreate(HabitBase):
    model_config = ConfigDict(title= "习惯创建")

class HabitUpdate(HabitBase):
    name: str | None = Field(None, max_length=255)
    description: str | None = None
    completed: bool | None = False
    duration: int | None = None

    model_config = ConfigDict(title= "习惯更新")

class HabitLogCreate(BaseModel):
    date: datetime | None = None

class HabitLogOut(BaseModel):
    id: int
    date: datetime

    model_config = ConfigDict(from_attributes=True, title= "打卡日志详情")

class HabitOut(HabitBase):
    id: int
    logs: list[HabitLogOut] = []

    model_config = ConfigDict(from_attributes=True, title= "习惯详情")

class PomodoroStart(BaseModel):
    """番茄钟启动"""
    work_minutes: Annotated[int, Field(ge=5, le=120, title="专注时长（分钟）")] = 25
    break_minutes: Annotated[int, Field(ge=1, le=60, title="休息时长（分钟）")] = 5
    model_config = ConfigDict(title="番茄钟启动")

class PomodoroOut(BaseModel):
    """番茄钟详情"""
    id: int
    start_at: datetime
    end_at: datetime | None
    work_minutes: int
    break_minutes: int
    planned_seconds: int
    actual_seconds: int | None
    completed: bool

    model_config = ConfigDict(from_attributes=True, title="番茄钟详情")