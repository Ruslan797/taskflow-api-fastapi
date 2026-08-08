from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.database.db import get_db
from app.models.tasks import Task
from app.models.users import User
from app.services import task_service


def get_current_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Task:
    task = task_service.get_task(
        db,
        task_id,
    )

    if (
        task is None
        or task.owner_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task