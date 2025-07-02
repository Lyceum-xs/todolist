from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta

from . import models, schemas, crud

class TaskService:
    @staticmethod
    def create_task(db: Session, task_data: dict) -> schemas.TaskOut:
        """创建任务"""
        if task_data.get("parent_id") == 0:
            task_data["parent_id"] = None

        validated_data = schemas.TaskCreate(**task_data)

        # 检查父任务是否存在
        if validated_data.parent_id is not None:
            if not crud.get_task(db, validated_data.parent_id):
                raise ValueError(f"父任务ID {validated_data.parent_id} 不存在")

        task = crud.create_task(db, validated_data)
        return schemas.TaskOut.model_validate(task)

    @staticmethod
    def get_task(db: Session, task_id: int) -> schemas.TaskOut:
        """获取单个任务"""
        task = crud.get_task(db, task_id)
        if not task:
            raise ValueError("任务不存在")
        return schemas.TaskOut.model_validate(task)

    @staticmethod
    def get_all_tasks(db: Session, status: str | None) -> list[schemas.TaskOut]:
        """获取任务列表并排序"""
        tasks_from_db = crud.get_tasks_by_status(db, status)
        # 按优先级排序
        tasks_from_db.sort(key=lambda t: t.priority_parameter, reverse=True)
        return [schemas.TaskOut.model_validate(task) for task in tasks_from_db]

    @staticmethod
    def update_task(db: Session, task_id: int, update_data: dict) -> schemas.TaskOut:
        """更新任务"""
        if "parent_id" in update_data and update_data["parent_id"] == 0:
            update_data["parent_id"] = None
        validated_data = schemas.TaskUpdate(**update_data)

        if validated_data.parent_id is not None:
            if not crud.get_task(db, validated_data.parent_id):
                raise ValueError(f"父任务ID {validated_data.parent_id} 不存在")
            # 防止将任务设置为自己的父任务
            if validated_data.parent_id == task_id:
                raise ValueError("不能将任务设置为自己的父任务")
        updated_task = crud.update_task(db, task_id, validated_data)
        if not updated_task:
            raise ValueError("任务不存在")
        return schemas.TaskOut.model_validate(updated_task)

    @staticmethod
    def delete_task(db: Session, task_id: int):
        """删除任务"""
        if not crud.delete_task(db, task_id):
            raise ValueError("任务不存在")

    @staticmethod
    def get_subtasks(db: Session, parent_id: int) -> list[schemas.TaskOut]:
        """获取子任务"""
        if not crud.get_task(db, parent_id):
            raise ValueError("父任务不存在")
        subtasks = crud.get_subtasks(db, parent_id)
        return [schemas.TaskOut.model_validate(task) for task in subtasks]

    @staticmethod
    def search_tasks(db: Session, query: str) -> list[schemas.TaskOut]:
        """搜索任务"""
        tasks = crud.search_tasks_by_name(db, query)
        return [schemas.TaskOut.model_validate(task) for task in tasks]


class HabitService:
    @staticmethod
    def create_habit(db: Session, habit_data: dict) -> schemas.HabitOut:
        """创建习惯"""
        validated_data = schemas.HabitCreate(**habit_data)

        # 检查习惯名称是否已存在
        if crud.get_habit_by_name(db, validated_data.name):
            raise ValueError(f"习惯 '{validated_data.name}' 已存在。")

        habit = crud.create_habit(db, validated_data)
        return schemas.HabitOut.model_validate(habit)

    @staticmethod
    def get_all_habits(db: Session) -> list[schemas.HabitOut]:
        """获取所有习惯"""
        habits = crud.get_all_habits(db)
        return [schemas.HabitOut.model_validate(habit) for habit in habits]


    @staticmethod
    def delete_habit(db: Session, habit_id: int):
        """删除习惯"""
        if not crud.delete_habit:
            raise ValueError("习惯不存在")

    @staticmethod
    def create_habit_log(db: Session, habit_id: int, log_data: dict) -> schemas.HabitLogOut:
        """创建打卡记录"""
        # 检查习惯是否存在
        if not crud.get_habit(db, habit_id):
            raise ValueError("习惯不存在")

        log_date = log_data.get("date")
        if isinstance(log_date, datetime):
            log_date = log_date.date()

        # 检查是否重复打卡
        if crud.get_log_by_date(db, habit_id, log_date):
            raise ValueError("今日已打卡，请勿重复操作。")

        log = crud.create_habit_log(db, habit_id, log_date)
        return schemas.HabitLogOut.model_validate(log)

    @staticmethod
    def get_habit_logs(db: Session, habit_id: int) -> list[schemas.HabitLogOut]:
        """获取一个习惯的所有打卡记录"""
        if not crud.get_habit(db, habit_id):
            raise ValueError("习惯不存在")
        logs = crud.get_logs_by_habit_id(db, habit_id)
        return [schemas.HabitLogOut.model_validate(log) for log in logs]

    @staticmethod
    def get_habit_streak(db: Session, habit_id: int) -> int:
        """计算持续打卡天数"""
        if not crud.get_habit(db, habit_id):
            raise ValueError("习惯不存在")

        logs = crud.get_logs_by_habit_id(db, habit_id)
        if not logs:
            return 0

        log_dates = {log.date for log in logs}
        streak = 0
        today = date.today()

        start_date = today
        # 如果今天没打卡，从昨天开始算
        if today not in log_dates:
            start_date = today - timedelta(days=1)
            # 如果昨天也没打卡，连击为0
            if start_date not in log_dates:
                return 0

        current_date = start_date
        while current_date in log_dates:
            streak += 1
            current_date -= timedelta(days=1)

        return streak
    
    @staticmethod
    def delete_habit(db: Session, habit_id: int):
        """删除习惯"""
        # 调用crud层来执行数据库删除操作
        if not crud.delete_habit(db, habit_id):
            raise ValueError("习惯不存在")
