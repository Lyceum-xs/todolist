from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
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
    urgency: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    parent_id: Mapped[int | None] = mapped_column(ForeignKey("tasks.id"))
    subtasks: Mapped[list["Task"]] = relationship(
        "Task",
        backref="parent",
<<<<<<< HEAD
        remote_side=[id]
=======
        remote_side=[id],
        cascade="all, delete-orphan"
>>>>>>> 1325033 (更新排序函数)
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

        urgency_value = 1 if self.urgency else 0
        importance_value = 1 if self.importance else 0

        # 处理截止日期属性，如果有截止日期，计算距离当前时间的天数；没有则设为一个较大值
        if self.due_date:
            days_to_due = (self.due_date - datetime.now(timezone.utc)).days
            days_to_due = max(days_to_due, 0)
            due_date_value = 1 / (days_to_due + 1)
        else:
            due_date_value = 0

        priority = (
            importance_value * importance_weight +
            urgency_value * urgent_weight +
            due_date_value * due_date_weight
        )
        return priority
