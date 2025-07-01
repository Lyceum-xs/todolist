from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, timedelta

from ..db import get_db
from .. import models, schemas

router = APIRouter(prefix="/habits", tags=["习惯"])


@router.post("", response_model=schemas.HabitOut, summary="创建习惯")
def create_habit(habit: schemas.HabitCreate, db: Session = Depends(get_db)):
    db_habit = models.Habit(**habit.model_dump())
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit


@router.get("", response_model=list[schemas.HabitOut], summary="习惯列表")
def list_habits(db: Session = Depends(get_db)):
    return db.query(models.Habit).all()


@router.post("/{habit_id}/log", summary="打卡")
def check_in(habit_id: int, body: schemas.HabitLogCreate, db: Session = Depends(get_db)):
    h = db.get(models.Habit, habit_id)
    if not h:
        raise HTTPException(404, "Habit not found")
    # 判断是否到了可打卡的日期
    last_log = (
        db.query(models.HabitLog)
        .filter(models.HabitLog.habit_id == habit_id)
        .order_by(models.HabitLog.date.desc())
        .first()
    )
    if last_log and (body.date - last_log.date).days < h.interval:
        raise HTTPException(400, "Not yet time for next check-in")
    log = models.HabitLog(habit_id=habit_id, date=body.date)
    db.add(log)
    db.commit()
    return {"msg": "Check-in recorded"}