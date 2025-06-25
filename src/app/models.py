from datetime import datetime
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
    importance: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    urgent: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    parent_id: Mapped[int | None] = mapped_column(ForeignKey("tasks.id"))
    subtasks: Mapped[list["Task"]] = relationship("Task", backref="parent", remote_side=[id])

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )