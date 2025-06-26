from typing import List, Optional
from datetime import datetime
from ..models import Task
from ..database import load_tasks, save_tasks
from ..utils.validators import validate_date_format

class TaskAPI:
    """任务核心API（所有方法返回统一格式字典）"""
    
    @staticmethod
    def create_task(
        name: str,
        description: str = "",
        deadline: Optional[str] = None,
        is_urgent: bool = False,
        priority: int = 3
    ) -> dict:
        """
        创建新任务
        Returns:
            {"success": bool, "task": Task, "error": Optional[str]}
        """
        try:
            if deadline:
                validate_date_format(deadline)
                
            tasks = load_tasks()
            task_id = max(t.id for t in tasks) + 1 if tasks else 1
            task = Task(
                id=task_id,
                name=name,
                description=description,
                deadline=deadline,
                is_urgent=is_urgent,
                priority=priority
            )
            tasks.append(task)
            save_tasks(tasks)
            
            return {"success": True, "task": task, "error": None}
        except Exception as e:
            return {"success": False, "task": None, "error": str(e)}

    @staticmethod
    def get_tasks(
        status: Optional[str] = None,
        is_urgent: Optional[bool] = None,
        priority: Optional[int] = None
    ) -> dict:
        """
        获取过滤后的任务列表
        Returns:
            {"success": bool, "tasks": List[Task], "error": Optional[str]}
        """
        try:
            tasks = load_tasks()
            if status:
                tasks = [t for t in tasks if t.status == status]
            if is_urgent is not None:
                tasks = [t for t in tasks if t.is_urgent == is_urgent]
            if priority:
                tasks = [t for t in tasks if t.priority == priority]
                
            return {"success": True, "tasks": tasks, "error": None}
        except Exception as e:
            return {"success": False, "tasks": [], "error": str(e)}

    @staticmethod
    def update_task_status(task_id: int, new_status: str) -> dict:
        """更新任务状态"""
        try:
            tasks = load_tasks()
            task = next((t for t in tasks if t.id == task_id), None)
            if not task:
                return {"success": False, "error": "Task not found"}
                
            task.status = new_status
            save_tasks(tasks)
            return {"success": True, "task": task, "error": None}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def search_tasks(keyword: str) -> dict:
        """搜索任务"""
        try:
            tasks = [t for t in load_tasks() if keyword.lower() in t.name.lower()]
            return {"success": True, "tasks": tasks, "error": None}
        except Exception as e:
            return {"success": False, "tasks": [], "error": str(e)}