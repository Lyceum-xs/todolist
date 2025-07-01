from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date

from ..db import get_db
from .. import schemas, services

router = APIRouter(prefix="/habits", tags=["习惯"])


@router.post("", response_model=schemas.HabitOut, status_code=status.HTTP_201_CREATED, summary="创建习惯")
def create_habit(habit: schemas.HabitCreate, db: Session = Depends(get_db)):
    try:
        return services.HabitService.create_habit(db, habit.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=list[schemas.HabitOut], summary="习惯列表")
def list_habits(db: Session = Depends(get_db)):
    return services.HabitService.get_all_habits(db)


@router.post(
    "/{habit_id}/logs",
    response_model=schemas.HabitLogOut,
    status_code=status.HTTP_201_CREATED,
    summary="为习惯打卡（每日一次）"
)
def create_habit_log(habit_id: int, body: schemas.HabitLogCreate, db: Session = Depends(get_db)):
    log_data = body.model_dump()
    if log_data.get("date") is None:
        log_data["date"] = date.today()

    try:
        return services.HabitService.create_habit_log(db, habit_id, log_data)
    except ValueError as e:
        detail = str(e)
        if "今日已打卡" in detail:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)
        if "习惯不存在" in detail:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

@router.delete("/{habit_id:int}", status_code=status.HTTP_204_NO_CONTENT, summary="删除习惯")
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    try:
        services.HabitService.delete_habit(db, habit_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get(
    "/{habit_id}/logs",
    response_model=list[schemas.HabitLogOut],
    summary="获取习惯的打卡记录列表"
)
def get_habit_logs(habit_id: int, db: Session = Depends(get_db)):
    try:
        return services.HabitService.get_habit_logs(db, habit_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/{habit_id}/streak",
    response_model=int,
    summary="获取当前持续打卡天数"
)
def get_habit_streak(habit_id: int, db: Session = Depends(get_db)):
    try:
        return services.HabitService.get_habit_streak(db, habit_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
