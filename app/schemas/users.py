from sqlalchemy.orm import Session

from app.models.tasks import Task
from app.schemas.tasks import TaskCreate


def create_task(db: Session, task_data: TaskCreate) -> Task:
    task = Task(
        title=task_data.title,
        description=task_data.description,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task