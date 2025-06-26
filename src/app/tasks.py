# routers/tasks.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import SessionLocal
from .. import schemas, crud

router = APIRouter()

# 依赖项函数，用于获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 创建任务
@router.post("/tasks/", response_model=schemas.TaskOut, tags=["任务"])
def create_task_api(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, data=task)

# 获取单个任务
@router.get("/tasks/{task_id}", response_model=schemas.TaskOut, tags=["任务"])
def get_task_api(task_id: int, db: Session = Depends(get_db)):
    return crud.get_task(db, task_id)

# 获取多个任务
@router.get("/tasks/", response_model=list[schemas.TaskOut], tags=["任务"])
def get_tasks_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_tasks(db, skip=skip, limit=limit)

# 更新任务
@router.put("/tasks/{task_id}", response_model=schemas.TaskOut, tags=["任务"])
def update_task_api(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    return crud.update_task(db, task_id=task_id, data=task)

# 删除任务
@router.delete("/tasks/{task_id}", tags=["任务"])
def delete_task_api(task_id: int, db: Session = Depends(get_db)):
    result = crud.delete_task(db, task_id)
    return {"success": result}