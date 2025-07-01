from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..db import get_db

router = APIRouter(prefix="/tasks", tags=["任务"])

@router.post("", response_model=schemas.TaskOut, status_code=201, summary="创建任务")
def create_task(data: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, data)

@router.get("", response_model=list[schemas.TaskOut], summary="任务列表")
def list_tasks(
    status: str | None = Query(None, description="completed | pending | all"),
    db: Session = Depends(get_db),
):
    q = db.query(models.Task)
    if status == "completed":
        q = q.filter(models.Task.completed.is_(True))
    elif status == "pending":
        q = q.filter(models.Task.completed.is_(False))

    tasks = q.all()
    tasks.sort(key=lambda t: t.priority_parameter, reverse=True)
    return tasks

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

@router.get("/{task_id:int}/children",
            response_model=list[schemas.TaskOut],
            summary="获取任务的直接子任务列表")
def get_children_tasks(task_id: int, db: Session = Depends(get_db)):

    # 检查父任务是否存在
    parent_task = db.get(models.Task, task_id)
    if not parent_task:
        raise HTTPException(status_code=404, detail="Parent task not found")

    subtasks = crud.get_subtasks(db, parent_id=task_id)
    return subtasks
