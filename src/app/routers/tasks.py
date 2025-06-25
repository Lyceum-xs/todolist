from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, case, desc
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..db import SessionLocal

router = APIRouter(
    prefix="/tasks",
    tags=["任务"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=schemas.TaskOut, status_code=201, summary="创建任务")
def create_task(data: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, data)

@router.get("", response_model=list[schemas.TaskOut], summary="任务列表")
def list_tasks(
    status: str | None = Query(None, description="completed | pending | all"),
    order: str = Query("due_date", description="due_date | importance"),
    db: Session = Depends(get_db),
):
    q = db.query(models.Task)
    if status == "completed":
        q = q.filter(models.Task.completed.is_(True))
    elif status == "pending":
        q = q.filter(models.Task.completed.is_(False))

    if order == "importance":
        q = q.order_by(desc(models.Task.importance), asc(models.Task.due_date))
    else:
        q = q.order_by(case((models.Task.due_date.is_(None), 1), else_=0), asc(models.Task.due_date))
    return q.all()

@router.get("/{task_id:int}", response_model=schemas.TaskOut, summary="获取任务")
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(models.Task, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    return task

@router.patch("/{task_id:int}", response_model=schemas.TaskOut, summary="更新任务")
def update_task(task_id: int, patch: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = db.get(models.Task, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    for k, v in patch.dict(exclude_unset=True).items():
        setattr(task, k, v)
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id:int}", status_code=204, summary="删除任务")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(models.Task, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    db.delete(task)
    db.commit()

@router.get("/search", response_model=list[schemas.TaskOut], summary="搜索任务")
def search_tasks(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    return db.query(models.Task).filter(models.Task.name.like(f"%{q}%")).all()