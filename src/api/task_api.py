from datetime import datetime, timezone
from typing import List, Dict, Optional
from fastapi import HTTPException
from app.models import Task as TaskModel
from app.schemas import TaskCreate, TaskUpdate, TaskOut
from app.db import SessionLocal

class TaskAPI:
    """任务核心操作API"""
    
    @staticmethod
    def create_task(task_data: TaskCreate) -> TaskOut:
        """创建新任务"""
        db = SessionLocal()
        try:
            # 转换时区
            due_date = task_data.due_date.astimezone(timezone.utc) if task_data.due_date else None
            
            db_task = TaskModel(
                name=task_data.name,
                description=task_data.description,
                due_date=due_date,
                importance=task_data.importance,
                urgency=task_data.urgency,
                parent_id=task_data.parent_id
            )
            db.add(db_task)
            db.commit()
            db.refresh(db_task)
            return TaskOut.from_orm(db_task)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
        finally:
            db.close()

    @staticmethod
    def get_task(task_id: int) -> TaskOut:
        """获取单个任务"""
        db = SessionLocal()
        try:
            task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
            if not task:
                raise TaskNotFound(task_id)
            return TaskOut.from_orm(task)
        finally:
            db.close()

    @staticmethod
    def update_task(task_id: int, update_data: TaskUpdate) -> TaskOut:
        """更新任务"""
        db = SessionLocal()
        try:
            task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
            if not task:
                raise TaskNotFound(task_id)
                
            for field, value in update_data.dict(exclude_unset=True).items():
                if field == 'due_date' and value:
                    value = value.astimezone(timezone.utc)
                setattr(task, field, value)
                
            db.commit()
            db.refresh(task)
            return TaskOut.from_orm(task)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
        finally:
            db.close()

    @staticmethod
    def search_tasks(keyword: str, completed: Optional[bool] = None) -> List[TaskOut]:
        """搜索任务"""
        db = SessionLocal()
        try:
            query = db.query(TaskModel).filter(TaskModel.name.contains(keyword))
            if completed is not None:
                query = query.filter(TaskModel.completed == completed)
            return [TaskOut.from_orm(t) for t in query.all()]
        finally:
            db.close()