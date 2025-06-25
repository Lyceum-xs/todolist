from . import models
from sqlalchemy.orm import Session

from . import schemas

def create_task(db: Session, data: schemas.TaskCreate) -> models.Task:
    task = models.Task(**data.dict())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task