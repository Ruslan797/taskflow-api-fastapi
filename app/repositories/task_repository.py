from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tasks import Task


def get_task_by_id(
    db: Session,
    task_id: int,
) -> Task | None:
    statement = select(Task).where(
        Task.id == task_id,
    )

    return db.scalar(statement)


def get_tasks_by_owner(
    db: Session,
    owner_id: int,
) -> list[Task]:
    statement = (
        select(Task)
        .where(Task.owner_id == owner_id)
        .order_by(Task.id)
    )

    return list(
        db.scalars(statement).all()
    )


def create_task(
    db: Session,
    task: Task,
) -> Task:
    db.add(task)
    db.commit()
    db.refresh(task)

    return task