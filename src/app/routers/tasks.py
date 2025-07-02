from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Literal

from .. import schemas, services
from ..db import get_db

router = APIRouter(prefix="/tasks", tags=["任务"])

@router.post("", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED, summary="创建任务")
def create_task(data: schemas.TaskCreate, db: Session = Depends(get_db)):
    try:
        return services.TaskService.create_task(db, data.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("", response_model=list[schemas.TaskOut], summary="任务列表")
def list_tasks(
    status: Literal["completed", "pending", "all"] | None = Query(None, description="completed | pending | all"),
    db: Session = Depends(get_db),
):
    return services.TaskService.get_all_tasks(db, status)

@router.get("/{task_id:int}", response_model=schemas.TaskOut, summary="获取任务")
def get_task(task_id: int, db: Session = Depends(get_db)):
    try:
        return services.TaskService.get_task(db, task_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.patch("/{task_id:int}", response_model=schemas.TaskOut, summary="更新任务")
def update_task(task_id: int, patch: schemas.TaskUpdate, db: Session = Depends(get_db)):
    try:
        update_data = patch.model_dump(exclude_unset=True)
        return services.TaskService.update_task(db, task_id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{task_id:int}", status_code=status.HTTP_204_NO_CONTENT, summary="删除任务")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    try:
        services.TaskService.delete_task(db, task_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/search", response_model=list[schemas.TaskOut], summary="搜索任务")
def search_tasks(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    return services.TaskService.search_tasks(db, q)

@router.get("/{task_id:int}/children",
            response_model=list[schemas.TaskOut],
            summary="获取任务的直接子任务列表")
def get_children_tasks(task_id: int, db: Session = Depends(get_db)):
    try:
        return services.TaskService.get_subtasks(db, parent_id=task_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
@router.get("", response_model=list[schemas.TaskOut], summary="任务列表")
def list_tasks(
    status: Literal["completed", "pending", "all"] | None = Query(None, description="任务状态:completed | pending | all"),
    sort_by: Literal["priority", "id"] = Query("priority", description="排序方式:priority (优先级) | id (创建顺序)"),
    db: Session = Depends(get_db),
):
    return services.TaskService.get_all_tasks(db, status, sort_by)