from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.subtasks import Subtask
from app.models.tasks import Task
from app.schemas import SubtaskCreate, SubtaskUpdate


def get_subtask(
    db: Session,
    task_id: int,
    subtask_id: int,
) -> Subtask | None:
    statement = select(Subtask).where(
        Subtask.id == subtask_id,
        Subtask.task_id == task_id,
    )

    return db.scalar(statement)


def get_subtasks(
    db: Session,
    task_id: int,
) -> list[Subtask]:
    statement = (
        select(Subtask)
        .where(Subtask.task_id == task_id)
        .order_by(Subtask.id)
    )

    return list(db.scalars(statement).all())


def create_subtask(
    db: Session,
    task_id: int,
    subtask_data: SubtaskCreate,
) -> Subtask | None:
    task = db.get(Task, task_id)

    if task is None:
        return None

    subtask = Subtask(
        title=subtask_data.title,
        task_id=task_id,
    )

    db.add(subtask)
    db.commit()
    db.refresh(subtask)

    return subtask


def update_subtask(
    db: Session,
    task_id: int,
    subtask_id: int,
    subtask_data: SubtaskUpdate,
) -> Subtask | None:
    subtask = get_subtask(
        db,
        task_id,
        subtask_id,
    )

    if subtask is None:
        return None

    update_data = subtask_data.model_dump(
        exclude_unset=True,
    )

    for field, value in update_data.items():
        setattr(subtask, field, value)

    db.commit()
    db.refresh(subtask)

    return subtask


def delete_subtask(
    db: Session,
    task_id: int,
    subtask_id: int,
) -> bool:
    subtask = get_subtask(
        db,
        task_id,
        subtask_id,
    )

    if subtask is None:
        return False

    db.delete(subtask)
    db.commit()

    return True