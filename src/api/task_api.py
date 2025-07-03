# api/task_api.py
from datetime import datetime, timezone
from typing import List, Dict, Optional
from fastapi import HTTPException
from .exceptions import TaskNotFound, InvalidTaskData  # 明确导入异常类
from app.models import Task as TaskModel
from app.schemas import TaskCreate, TaskUpdate, TaskOut
from app.db import SessionLocal

class TaskAPI:
    """任务核心操作API"""

    @staticmethod
    def get_task(task_id: int) -> TaskOut:
        """获取单个任务"""
        db = SessionLocal()
        try:
            task = db.query(TaskModel).filter(TaskModel.id == task_id).first()  # 关键修正
            if not task:
                raise TaskNotFound(task_id)  # 使用已定义的异常类
            return TaskOut.from_orm(task)
        finally:
            db.close()

    @staticmethod
    def update_task(task_id: int, update_data: TaskUpdate) -> TaskOut:
        """更新任务（修正版）"""
        db = SessionLocal()
        try:
            task = db.query(TaskModel).filter(TaskModel.id == task_id).first()  # 关键修正
            if not task:
                raise TaskNotFound(task_id)
                
            # 更新字段逻辑保持不变
            for field, value in update_data.dict(exclude_unset=True).items():
                setattr(task, field, value)
                
            db.commit()
            db.refresh(task)
            return TaskOut.from_orm(task)
        except ValueError as e:
            db.rollback()
            raise InvalidTaskData(field="data", reason=str(e))
        finally:
            db.close()