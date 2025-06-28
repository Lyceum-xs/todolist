import sqlalchemy
from sqlalchemy.orm import Session
from . import models, schemas
from .db import db_session
from .crud import create_task, get_task, get_tasks, update_task, delete_task

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

    @staticmethod
    def get_task_with_children(task_id: int) -> schemas.TaskOut:
        with db_session() as db:
            task = db.query(models.Task).options(
                sqlalchemy.orm.joinedload(models.Task.subtasks)
            ).get(task_id)
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


class HabitService:
    """创建习惯"""
    @staticmethod
    def create_habit(habit_data: dict) -> schemas.HabitOut:
        with db_session() as db:
            try:
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
            habit = db.query(models.Habit).options(
                sqlalchemy.orm.joinedload(models.Habit.logs)
            ).get(habit_id)
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
                habit = db.query(models.Habit).get(habit_id)
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
                habit = db.query(models.Habit).get(habit_id)
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
                # 检查习惯是否存在
                habit = db.query(models.Habit).get(habit_id)
                if not habit:
                    raise ValueError("习惯不存在")

                validated_data = schemas.HabitLogCreate(**log_data)
                log = models.HabitLog(
                    habit_id=habit_id,
                    **validated_data.model_dump(exclude_unset=True)
                )

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
        with db_session() as db:
            # 检查习惯是否存在
            habit = db.query(models.Habit).get(habit_id)
            if not habit:
                raise ValueError("习惯不存在")

            logs = db.query(models.HabitLog).filter(
                models.HabitLog.habit_id == habit_id
            ).all()

            return [schemas.HabitLogOut.model_validate(log) for log in logs]
