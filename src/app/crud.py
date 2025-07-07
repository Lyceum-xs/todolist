from sqlalchemy.orm import Session
import sqlalchemy
from typing import Literal
from datetime import date

from . import models, schemas

# ---任务功能实现---

def create_task(db: Session, data: schemas.TaskCreate) -> models.Task:
    """创建新任务"""
    task = models.Task(**data.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_task(db: Session, task_id: int) -> models.Task | None:
    """通过ID获取任务"""
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks_by_status(db: Session, status: Literal["completed", "pending", "all"] | None) -> list[models.Task]:
    """根据完成状态获取任务列表"""
    q = db.query(models.Task)
    if status == "completed":
        q = q.filter(models.Task.completed == True)
    elif status == "pending":
        q = q.filter(models.Task.completed == False)
    return q.all()

def search_tasks_by_name(db: Session, name_query: str) -> list[models.Task]:
    """根据名称搜索任务"""
    return db.query(models.Task).filter(models.Task.name.like(f"%{name_query}%")).all()

def update_task(db: Session, task_id: int, data: schemas.TaskUpdate) -> models.Task | None:
    """更新任务状态"""
    task = get_task(db, task_id)
    if not task:
        return None

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int) -> bool:
    """删除任务"""
    task = get_task(db, task_id)
    if not task:
        return False

    db.delete(task)
    db.commit()
    return True

def get_subtasks(db: Session, parent_id: int) -> list[models.Task]:
    """获取一个任务的所有子任务"""
    return db.query(models.Task).filter(models.Task.parent_id == parent_id).all()

# --- 习惯功能 ---

def create_habit(db: Session, data: schemas.HabitCreate) -> models.Habit:
    """创建新习惯"""
    habit = models.Habit(**data.model_dump())
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit

def get_habit(db: Session, habit_id: int) -> models.Habit | None:
    """通过ID获取习惯及其打卡记录"""
    return db.query(models.Habit).options(
        sqlalchemy.orm.joinedload(models.Habit.logs)
    ).filter(models.Habit.id == habit_id).first()

def delete_habit(db: Session, habit_id: int) -> bool:
    """删除习惯"""
    habit = get_habit(db, habit_id)
    if not habit:
        return False

    db.delete(habit)
    db.commit()
    return True

def get_habit_by_name(db: Session, name: str) -> models.Habit | None:
    """通过名称获取习惯"""
    return db.query(models.Habit).filter(models.Habit.name == name).first()

def get_all_habits(db: Session) -> list[models.Habit]:
    """获取所有习惯及其打卡记录"""
    return db.query(models.Habit).options(
        sqlalchemy.orm.joinedload(models.Habit.logs)
    ).all()

def create_habit_log(db: Session, habit_id: int, log_date: date) -> models.HabitLog:
    """为习惯创建新的打卡记录"""
    log = models.HabitLog(habit_id=habit_id, date=log_date)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

def get_log_by_date(db: Session, habit_id: int, log_date: date) -> models.HabitLog | None:
    """根据习惯ID和日期获取打卡记录"""
    return db.query(models.HabitLog).filter_by(habit_id=habit_id, date=log_date).first()

def get_logs_by_habit_id(db: Session, habit_id: int) -> list[models.HabitLog]:
    """获取一个习惯的所有打卡记录"""
    return db.query(models.HabitLog).filter_by(habit_id=habit_id).order_by(models.HabitLog.date.desc()).all()

