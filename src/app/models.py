from datetime import datetime, timezone , date
from sqlalchemy import Boolean, DateTime, Date , ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    due_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    importance: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    urgent: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    parent_id: Mapped[int | None] = mapped_column(ForeignKey("tasks.id"))
    subtasks: Mapped[list["Task"]] = relationship(
        "Task",
        backref="parent",
        remote_side=[id],
        single_parent=True,
        cascade="all, delete-orphan" #删除父任务时，其所有子任务会被级联删除
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    @property
    #暂时实现一个简单的加权求和法，后续有优化拟合量化函数可以再改
    def priority_parameter(self):
        importance_weight = 0.45
        urgent_weight = 0.45
        due_date_weight = 0.1

        urgent_value = 1 if self.urgent else 0
        importance_value = 1 if self.important else 0

        # 处理截止日期属性，如果有截止日期，计算距离当前时间的天数；没有则设为一个较大值
        if self.due_date:
            days_to_due = (self.due_date - datetime.now(timezone.utc)).days
            days_to_due = max(days_to_due, 0)
            due_date_value = 1 / (days_to_due + 1)
        else:
            due_date_value = 0

        priority = (
            importance_value * importance_weight +
            urgent_value * urgent_weight +
            due_date_value * due_date_weight
        )
        return priority

class Habit(Base):
    __tablename__ = "habits"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    # 重复周期（天数），默认 1 = 每天
    interval: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    logs: Mapped[list["HabitLog"]] = relationship(
        "HabitLog", back_populates="habit", cascade="all, delete-orphan"
    )


class HabitLog(Base):
    __tablename__ = "habit_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id"), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    done: Mapped[bool] = mapped_column(Boolean, default=True)

    habit: Mapped["Habit"] = relationship("Habit", back_populates="logs")