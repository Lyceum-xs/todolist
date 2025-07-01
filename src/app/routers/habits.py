from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date

from ..db import get_db
from .. import schemas, services

router = APIRouter(prefix="/habits", tags=["习惯"])


@router.post("", response_model=schemas.HabitOut, status_code=status.HTTP_201_CREATED, summary="创建习惯")
def create_habit(habit: schemas.HabitCreate):
    try:
        return services.HabitService.create_habit(habit.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=list[schemas.HabitOut], summary="习惯列表")
def list_habits():
    return services.HabitService.get_all_habits()


@router.post(
    "/{habit_id}/logs",
    response_model=schemas.HabitLogOut,
    status_code=status.HTTP_201_CREATED,
    summary="为习惯打卡（每日一次）"
)
def create_habit_log(habit_id: int, body: schemas.HabitLogCreate):
    log_data = body.model_dump()
    if log_data.get("date") is None:
        log_data["date"] = date.today()

    try:
        created_log = services.HabitService.create_habit_log(habit_id, log_data)
        return created_log
    except ValueError as e:
        detail = str(e)
        # 如果是重复打卡，返回 409 Conflict 状态码
        if "今日已打卡" in detail:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)
        # 如果是习惯不存在，返回 404 Not Found
        if "习惯不存在" in detail:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
        # 其他值错误
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


@router.get(
    "/{habit_id}/logs",
    response_model=list[schemas.HabitLogOut],
    summary="获取习惯的打卡记录列表"
)
def get_habit_logs(habit_id: int):
    try:
        return services.HabitService.get_habit_logs(habit_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/{habit_id}/streak",
    response_model=int,
    summary="【新增】获取当前持续打卡天数"
)
def get_habit_streak(habit_id: int):
    """
    计算并返回一个习惯从今天或昨天开始的连续打卡天数。
    - 如果今天和昨天都没打卡，则连击中断，返回 0。
    """
    try:
        return services.HabitService.get_habit_streak(habit_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))