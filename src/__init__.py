__version__ = "1.0.0"

from .database import load_tasks, save_tasks, generate_id
from .models import Task
from .todo import (
    add_task,
    list_tasks,
    update_status,
    update_status_by_name,
    delete_task,
    delete_tasks_by_name,
    filter_tasks,
    search_tasks,
)

__all__ = [
    "load_tasks", "save_tasks", "generate_id",
    "Task",
    "add_task", "list_tasks",
    "update_status", "update_status_by_name",
    "delete_task", "delete_tasks_by_name",
    "filter_tasks", "search_tasks",
]