from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tasks import Task
from app.schemas import TaskCreate, TaskUpdate


def get_task(
    db: Session,
    task_id: int,
) -> Task | None:
    statement = select(Task).where(Task.id == task_id)

    return db.scalar(statement)


def get_tasks(db: Session) -> list[Task]:
    statement = select(Task).order_by(Task.id)

    return list(db.scalars(statement).all())


def create_task(
    db: Session,
    task_data: TaskCreate,
) -> Task:
    task = Task(
        title=task_data.title,
        description=task_data.description,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def update_task(
    db: Session,
    task_id: int,
    task_data: TaskUpdate,
) -> Task | None:
    task = get_task(db, task_id)

    if task is None:
        return None

    update_data = task_data.model_dump(
        exclude_unset=True,
    )

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task

def delete_task(
    db: Session,
    task_id: int,
) -> bool:
    task = get_task(db, task_id)

    if task is None:
        return False

    db.delete(task)
    db.commit()

    return True