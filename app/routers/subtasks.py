from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_task
from app.database.db import get_db
from app.models.tasks import Task
from app.schemas import (
    SubtaskCreate,
    SubtaskResponse,
    SubtaskUpdate,
)
from app.services import subtask_service


from app.core.auth import get_current_user
from app.models.users import User

router = APIRouter(
    prefix="/tasks/{task_id}/subtasks",
    tags=["Subtasks"],
)

@router.get(
    "",
    response_model=list[SubtaskResponse],
)
def get_subtasks(
    current_task: Task = Depends(get_current_task),
    db: Session = Depends(get_db),
) -> list[SubtaskResponse]:
    return subtask_service.get_subtasks(
        db,
        current_task.id,
    )


@router.get(
    "/{subtask_id}",
    response_model=SubtaskResponse,
)
def get_subtask(
    subtask_id: int,
    current_task: Task = Depends(get_current_task),
    db: Session = Depends(get_db),
) -> SubtaskResponse:
    subtask = subtask_service.get_subtask(
        db,
        current_task.id,
        subtask_id,
    )

    if subtask is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subtask not found",
        )

    return subtask

@router.post(
    "",
    response_model=SubtaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_subtask(
    subtask_data: SubtaskCreate,
    current_task: Task = Depends(get_current_task),
    db: Session = Depends(get_db),
) -> SubtaskResponse:
    subtask = subtask_service.create_subtask(
        db,
        current_task.id,
        subtask_data,
    )

    if subtask is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return subtask


@router.patch(
    "/{subtask_id}",
    response_model=SubtaskResponse,
)
def update_subtask(
    subtask_id: int,
    subtask_data: SubtaskUpdate,
    current_task: Task = Depends(get_current_task),
    db: Session = Depends(get_db),
) -> SubtaskResponse:
    subtask = subtask_service.update_subtask(
        db,
        current_task.id,
        subtask_id,
        subtask_data,
    )

    if subtask is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subtask not found",
        )

    return subtask


@router.delete(
    "/{subtask_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_subtask(
    subtask_id: int,
    current_task: Task = Depends(get_current_task),
    db: Session = Depends(get_db),
) -> None:
    deleted = subtask_service.delete_subtask(
        db,
        current_task.id,
        subtask_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subtask not found",
        )