from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date

from ..db import get_db
from .. import schemas, services

router = APIRouter(prefix="/habits", tags=["习惯"])

@router.post("", response_model=schemas.HabitOut, status_code=status.HTTP_201_CREATED, summary="创建习惯")
def create_habit(habit: schemas.HabitCreate, db: Session = Depends(get_db)):
    try:
        return services.HabitService.create_habit(habit.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=list[schemas.HabitOut], summary="习惯列表")
def list_habits(db: Session = Depends(get_db)):
    return services.HabitService.get_all_habits()


@router.post(
    "/{habit_id}/logs",
    response_model=schemas.HabitLogOut,
    status_code=status.HTTP_201_CREATED,
    summary="打卡"
)
def create_habit_log(habit_id: int, body: schemas.HabitLogCreate, db: Session = Depends(get_db)):
    log_data = body.model_dump()
    if log_data.get("date") is None:
        log_data["date"] = date.today()

    try:
        # 使用 Service 层来创建打卡记录，保持逻辑分离
        created_log = services.HabitService.create_habit_log(habit_id, log_data)
        return created_log
    except ValueError as e:
        # 如果 Service 层抛出异常（例如习惯不存在），则返回 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"创建打卡记录失败: {e}")
    
@router.get(
    "/{habit_id}/logs",
    response_model=list[schemas.HabitLogOut],
    summary="获取习惯的打卡记录列表"
)
def get_habit_logs(habit_id: int, db: Session = Depends(get_db)):
    """
    获取指定习惯的所有打卡记录。
    """
    try:
        # 调用服务层的方法来获取数据
        logs = services.HabitService.get_habit_logs(habit_id)
        return logs
    except ValueError as e:
        # 如果服务层抛出异常（例如习惯不存在），则返回 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
