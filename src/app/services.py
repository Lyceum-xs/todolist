import sqlalchemy
from sqlalchemy.orm import Session
from . import models, schemas
from .db import db_session
from .crud import create_task, get_task, get_tasks, update_task, delete_task

class TaskService:

    @staticmethod
    def _to_dict(task: models.Task) -> dict:
        return {
            "id": task.id,
            "name": task.name,
            "completed": task.completed,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "priority": task.priority_parameter,
            "subtasks": [TaskService._to_dict(sub) for sub in task.subtasks]
        }

    """创建任务"""
    @staticmethod
    def create_task(task_data: dict) -> dict:
        with db_session() as db:
            try:
                validated_data = schemas.TaskCreate(**task_data)
                task = create_task(db, validated_data)
                return TaskService._to_dict(task)
            except Exception as e:
                raise ValueError(f"创建失败: {str(e)}")

    @staticmethod
    def get_task_with_children(task_id: int) -> dict:
        with db_session() as db:
            task = db.query(models.Task).options(
                sqlalchemy.orm.joinedload(models.Task.subtasks)
            ).get(task_id)
            if not task:
                raise ValueError("任务不存在")
            return TaskService._to_dict(task)

    """获取单个任务"""
    @staticmethod
    def get_task(task_id: int) -> dict | None:
        with db_session() as db:
            if task := get_task(db, task_id):
                return TaskService._to_dict(task)
            return None


    """获取所有任务"""
    @staticmethod
    def get_all_tasks() -> list[dict]:
        with db_session() as db:
            return [TaskService._to_dict(task) for task in get_tasks(db)]

    """更新任务"""
    @staticmethod
    def update_task(task_id: int, update_data: dict) -> dict:
        with db_session() as db:
            try:
                validated_data = schemas.TaskUpdate(**update_data)
                if task := update_task(db, task_id, validated_data):
                    return TaskService._to_dict(task)
                raise ValueError("任务不存在")
            except Exception as e:
                raise ValueError(f"更新失败: {str(e)}")

    """删除任务"""
    @staticmethod
    def delete_task(task_id: int) -> bool:
        with db_session() as db:
            try:
                success = delete_task(db, task_id)
                if not success:
                    raise ValueError("任务不存在")
                return True
            except Exception as e:
                raise ValueError(f"删除失败: {str(e)}")