import sqlalchemy
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from . import models, schemas
from .db import db_session
from .crud import create_task, get_task, get_tasks, update_task, delete_task

try:
    from datetime import UTC  # Python 3.11+
except ImportError:
    from datetime import timezone
    UTC = timezone.utc

class TaskService:

    """创建任务"""
    @staticmethod
    def create_task(task_data: dict) -> schemas.TaskOut:
        with db_session() as db:
            try:
                validated_data = schemas.TaskCreate(**task_data)
                task = create_task(db, validated_data)
                return schemas.TaskOut.model_validate(task)
            except Exception as e:
                raise ValueError(f"创建失败: {str(e)}")

    """获取子任务"""
    @staticmethod
    def get_task_with_children(task_id: int) -> schemas.TaskOut:
        with db_session() as db:
            task = db.get(
                models.Task,
                task_id,
                options=[sqlalchemy.orm.joinedload(models.Task.subtasks)]
            )
            if not task:
                raise ValueError("任务不存在")
            return schemas.TaskOut.model_validate(task)

    """获取单个任务"""
    @staticmethod
    def get_task(task_id: int) -> dict | None:
        with db_session() as db:
            if task := get_task(db, task_id):
                return schemas.TaskOut.model_validate(task)
            return None


    """获取所有任务"""
    @staticmethod
    def get_all_tasks() -> list[dict]:
        with db_session() as db:
            return [schemas.TaskOut.model_validate(task) for task in get_tasks(db)]

    """更新任务"""
    @staticmethod
    def update_task(task_id: int, update_data: dict) -> dict:
        with db_session() as db:
            try:
                validated_data = schemas.TaskUpdate(**update_data)
                if task := update_task(db, task_id, validated_data):
                    return schemas.TaskOut.model_validate(task)
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

    """检查父任务是否存在且有效"""
    @staticmethod
    def _validate_parent(db: Session, parent_id: int | None) -> None:
        if parent_id is not None:
            parent = get_task(db, parent_id)
            if not parent:
                raise ValueError(f"父任务ID {parent_id} 不存在")
            # 可选：防止循环引用
            if parent.parent_id == parent_id:
                raise ValueError("不能设置自己为父任务")

class HabitService:
    """创建习惯"""
    @staticmethod
    def create_habit(habit_data: dict) -> schemas.HabitOut:
        with db_session() as db:
            try:
                # 检查习惯名称是否已存在
                if db.query(models.Habit).filter_by(name=habit_data.get("name")).first():
                    raise ValueError(f"习惯 '{habit_data.get('name')}' 已存在。")
                
                validated_data = schemas.HabitCreate(**habit_data)
                habit = models.Habit(**validated_data.model_dump())
                db.add(habit)
                db.commit()
                db.refresh(habit)
                return schemas.HabitOut.model_validate(habit)
            except Exception as e:
                db.rollback()
                raise ValueError(f"创建习惯失败: {str(e)}")

    """获取单个习惯"""
    @staticmethod
    def get_habit(habit_id: int) -> schemas.HabitOut | None:
        with db_session() as db:
            habit = db.get(
                models.Habit,
                habit_id,
                options=[sqlalchemy.orm.joinedload(models.Habit.logs)]
            )
            if not habit:
                return None
            return schemas.HabitOut.model_validate(habit)

    """获取所有习惯"""
    @staticmethod
    def get_all_habits() -> list[schemas.HabitOut]:
        with db_session() as db:
            habits = db.query(models.Habit).options(
                sqlalchemy.orm.joinedload(models.Habit.logs)
            ).all()
            return [schemas.HabitOut.model_validate(habit) for habit in habits]

    """更新习惯"""
    @staticmethod
    def update_habit(habit_id: int, update_data: dict) -> schemas.HabitOut:
        with db_session() as db:
            try:
                validated_data = schemas.HabitUpdate(**update_data)
                habit = db.get(models.Habit, habit_id)
                if not habit:
                    raise ValueError("习惯不存在")

                for key, value in validated_data.model_dump(exclude_unset=True).items():
                    setattr(habit, key, value)

                db.commit()
                db.refresh(habit)
                return schemas.HabitOut.model_validate(habit)
            except Exception as e:
                db.rollback()
                raise ValueError(f"更新习惯失败: {str(e)}")

    """删除习惯"""
    @staticmethod
    def delete_habit(habit_id: int) -> bool:
        with db_session() as db:
            try:
                habit = db.get(models.Habit, habit_id)
                if not habit:
                    raise ValueError("习惯不存在")

                db.delete(habit)
                db.commit()
                return True
            except Exception as e:
                db.rollback()
                raise ValueError(f"删除习惯失败: {str(e)}")

    """创建习惯打卡记录"""
    @staticmethod
    def create_habit_log(habit_id: int, log_data: dict) -> schemas.HabitLogOut:
        with db_session() as db:
            try:
                habit = db.get(models.Habit, habit_id)
                if not habit:
                    raise ValueError("习惯不存在")

                log_date = log_data.get("date", date.today())
                if isinstance(log_date, datetime):
                    log_date = log_date.date()

                # --- 检查今天是否已打卡 ---
                existing_log = db.query(models.HabitLog).filter_by(
                    habit_id=habit_id, date=log_date
                ).first()
                if existing_log:
                    raise ValueError("今日已打卡，请勿重复操作。")

                log = models.HabitLog(habit_id=habit_id, date=log_date)
                db.add(log)
                db.commit()
                db.refresh(log)
                return schemas.HabitLogOut.model_validate(log)
            except Exception as e:
                db.rollback()
                raise ValueError(f"创建打卡记录失败: {str(e)}")

    """获取习惯的打卡记录"""
    @staticmethod
    def get_habit_logs(habit_id: int) -> list[schemas.HabitLogOut]:
        # (此方法无需修改)
        with db_session() as db:
            habit = db.get(models.Habit, habit_id)
            if not habit:
                raise ValueError("习惯不存在")
            logs = db.query(models.HabitLog).filter(
                models.HabitLog.habit_id == habit_id
            ).all()
            return [schemas.HabitLogOut.model_validate(log) for log in logs]

    """获取持续打卡天数"""
    @staticmethod
    def get_habit_streak(habit_id: int) -> int:
        with db_session() as db:
            if not db.get(models.Habit, habit_id):
                raise ValueError("习惯不存在")

            logs = db.query(models.HabitLog.date).filter_by(
                habit_id=habit_id
            ).order_by(models.HabitLog.date.desc()).all()

            if not logs:
                return 0

            streak = 0
            today = date.today()
            log_dates = {log.date for log in logs}

            # 检查最近的打卡是否是今天或昨天
            if today not in log_dates and (today - timedelta(days=1)) not in log_dates:
                return 0

            # 从今天或昨天开始，向前计算连续天数
            current_date = today
            while current_date in log_dates:
                streak += 1
                current_date -= timedelta(days=1)

            return streak
