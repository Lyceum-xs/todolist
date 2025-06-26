from datetime import datetime, timedelta
from typing import Dict, List
from sqlalchemy import func, and_
from app.models import Task
from app.db import SessionLocal
from .task_api import TaskOut

class StatsAPI:
    """任务数据分析API"""
    
    @staticmethod
    def get_completion_rate() -> Dict[str, float]:
        """获取任务完成率"""
        db = SessionLocal()
        try:
            total = db.query(func.count(Task.id)).scalar()
            if not total:
                return {"rate": 0.0}
                
            completed = db.query(func.count(Task.id)).filter(Task.completed == True).scalar()
            return {"rate": round(completed / total * 100, 2)}
        finally:
            db.close()

    @staticmethod
    def get_priority_matrix() -> Dict[str, int]:
        """获取四象限任务分布"""
        db = SessionLocal()
        try:
            return {
                "重要紧急": db.query(Task).filter(and_(Task.importance == True, Task.urgency == True)).count(),
                "重要不紧急": db.query(Task).filter(and_(Task.importance == True, Task.urgency == False)).count(),
                "不重要紧急": db.query(Task).filter(and_(Task.importance == False, Task.urgency == True)).count(),
                "不重要不紧急": db.query(Task).filter(and_(Task.importance == False, Task.urgency == False)).count()
            }
        finally:
            db.close()

    @staticmethod
    def get_upcoming_tasks(days: int = 3) -> List[TaskOut]:
        """获取临近截止的任务"""
        db = SessionLocal()
        try:
            cutoff = datetime.utcnow() + timedelta(days=days)
            tasks = db.query(Task).filter(
                Task.due_date <= cutoff,
                Task.completed == False
            ).order_by(Task.due_date).all()
            return [TaskOut.from_orm(t) for t in tasks]
        finally:
            db.close()