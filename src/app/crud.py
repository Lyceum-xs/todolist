from . import models
from sqlalchemy.orm import Session

from . import schemas

def create_task(db: Session, data: schemas.TaskCreate) -> models.Task:
    task = models.Task(**data.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_task(db: Session, task_id: int) -> models.Task | None:
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_tasks(db: Session, skip: int = 0, limit: int = 100) -> list[models.Task]:
    return db.query(models.Task).offset(skip).limit(limit).all()

def update_task(
    db: Session,
    task_id: int,
    data: schemas.TaskUpdate
) -> models.Task | None:
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        return None

    # 更新字段（仅更新 data 中提供的值）
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int) -> bool:
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        return False

    db.delete(task)
    db.commit()
    return True

# --------------------------------------------------------------------------- #
# 子任务相关操作
# --------------------------------------------------------------------------- #

def get_children_count(db: Session, task_id: int) -> int:
    return db.query(models.Task).filter(models.Task.parent_id == task_id).count()


def bfs_subtree(db: Session, task_id: int) -> list[models.Task] | None:
    root = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not root:
        return None

    result: list[models.Task] = []
    queue: list[models.Task] = [root]
    while queue:
        node = queue.pop(0)
        result.append(node)
        queue.extend(node.subtasks)
    return result


def dfs_subtree(db: Session, task_id: int) -> list[models.Task] | None:
    root = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not root:
        return None

    result: list[models.Task] = []
    def _dfs(node: models.Task):
        result.append(node)
        for child in node.subtasks:
            _dfs(child)

    _dfs(root)
    return result
