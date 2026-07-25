from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas import (
    SubtaskCreate,
    SubtaskResponse,
    SubtaskUpdate,
)
from app.services import subtask_service

router = APIRouter(
    prefix="/tasks/{task_id}/subtasks",
    tags=["Subtasks"],
)


@router.get(
    "",
    response_model=list[SubtaskResponse],
)
def get_subtasks(
    task_id: int,
    db: Session = Depends(get_db),
) -> list[SubtaskResponse]:
    return subtask_service.get_subtasks(
        db,
        task_id,
    )


@router.get(
    "/{subtask_id}",
    response_model=SubtaskResponse,
)
def get_subtask(
    task_id: int,
    subtask_id: int,
    db: Session = Depends(get_db),
) -> SubtaskResponse:
    subtask = subtask_service.get_subtask(
        db,
        task_id,
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
    task_id: int,
    subtask_data: SubtaskCreate,
    db: Session = Depends(get_db),
) -> SubtaskResponse:
    subtask = subtask_service.create_subtask(
        db,
        task_id,
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
    task_id: int,
    subtask_id: int,
    subtask_data: SubtaskUpdate,
    db: Session = Depends(get_db),
) -> SubtaskResponse:
    subtask = subtask_service.update_subtask(
        db,
        task_id,
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
    task_id: int,
    subtask_id: int,
    db: Session = Depends(get_db),
) -> None:
    deleted = subtask_service.delete_subtask(
        db,
        task_id,
        subtask_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subtask not found",
        )