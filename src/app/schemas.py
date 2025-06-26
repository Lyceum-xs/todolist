from datetime import datetime
from datetime import date
from pydantic import BaseModel, Field , ConfigDict

class TaskBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: str | None = None
    due_date: datetime | None = None
    importance: bool = False
    urgent: bool = False
    parent_id: int | None = None

    class Config:
        title = "任务基础信息"

class TaskCreate(TaskBase):
    class Config:
        title = "任务创建"

class TaskUpdate(BaseModel):
    name: str | None = Field(None, max_length=255)
    description: str | None = None
    due_date: datetime | None = None
    completed: bool | None = False
    importance: bool | None = False
    urgent: bool | None = False

    class Config:
        title = "任务更新"

class TaskOut(TaskBase):
    id: int
    completed: bool

    class Config:
        orm_mode = True
        title = "任务详情"

class HabitBase(BaseModel):
    name: str = Field(..., max_length=128)
    interval: int = Field(1, ge=1, le=30)

class HabitCreate(HabitBase):
    pass

class HabitOut(HabitBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class HabitLogCreate(BaseModel):
    date: date