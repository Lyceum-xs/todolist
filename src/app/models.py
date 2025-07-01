from __future__ import annotations
from datetime import datetime, timezone
from datetime import date as da
from sqlalchemy import Boolean, DateTime, Date , ForeignKey, Integer, String
import sqlalchemy
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

    # 单个父任务（uselist=False）
    parent: Mapped["Task"] = relationship(
        "Task",
        remote_side=[id],
        back_populates="subtasks",
        uselist=False
    )

    # 子任务列表
    subtasks: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="parent",
        cascade="all, delete-orphan",
        single_parent=True
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
    def priority_parameter(self) -> float:
        """
        计算任务优先级 (0~1)。加入时区兼容处理，避免比较
        “offset‑aware” 与 “offset‑naive” datetime 抛错。
        """
        if self.completed:
            return 0.0

        importance_weight = 0.45
        urgent_weight = 0.45
        due_date_weight = 0.10

        importance_value = 1 if self.importance else 0
        urgent_value = 1 if self.urgent else 0

        now = datetime.now(timezone.utc)  # 始终使用带时区的当前时间

        if self.due_date:
            due = self.due_date

            # 若数据库里存储的是 naive datetime，则假定为 UTC
            if due.tzinfo is None or due.tzinfo.utcoffset(due) is None:
                due = due.replace(tzinfo=timezone.utc)

            if due < now:
                due_date_value = 1.0  # 已超期
            else:
                days_to_due = max((due - now).days, 0)
                due_date_value = 1 / (days_to_due + 1)
        else:
            due_date_value = 0.0  # 无截止日期

        return (
            importance_value * importance_weight
            + urgent_value * urgent_weight
            + due_date_value * due_date_weight
        )


class Habit(Base):
    __tablename__ = "habits"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    duration: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    logs: Mapped[list["HabitLog"]] = relationship(
        "HabitLog", back_populates="habit", cascade="all, delete-orphan"
    )

class HabitLog(Base):
    __tablename__ = "habit_logs"
    __table_args__ = (
        sqlalchemy.UniqueConstraint('habit_id', 'date', name='uq_habit_date'),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id"), nullable=False)
    date: Mapped[da] = mapped_column(Date, default=lambda: da.today(), nullable=False)

    habit: Mapped["Habit"] = relationship("Habit", back_populates="logs")

class PomodoroSession(Base):
    __tablename__ = "pomodoros"

    id: Mapped[int] = mapped_column(primary_key=True)
    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    work_minutes: Mapped[int] = mapped_column(Integer, default=25, nullable=False)
    break_minutes: Mapped[int] = mapped_column(Integer, default=5, nullable=False)

    planned_seconds: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_seconds: Mapped[int | None] = mapped_column(Integer)

    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)