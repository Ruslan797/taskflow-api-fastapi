from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas import TaskCreate, TaskResponse, TaskUpdate
from app.services import task_service

from app.core.auth import get_current_user
from app.models.users import User

from app.core.dependencies import get_current_task
from app.models.tasks import Task

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.get(
    "",
    response_model=list[TaskResponse],
)
def get_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[TaskResponse]:
    return task_service.get_tasks(
        db,
        current_user.id,
)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
def get_task(
    current_task: Task = Depends(get_current_task),
) -> TaskResponse:
    return current_task


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskResponse:
    return task_service.create_task(
        db,
        task_data,
        current_user.id,
    )


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
)
def update_task(
    task_data: TaskUpdate,
    current_task: Task = Depends(get_current_task),
    db: Session = Depends(get_db),
) -> TaskResponse:

    task = task_service.update_task(
        db,
        current_task.id,
        task_data,
    )

    return task

    

@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)

def delete_task(
    current_task: Task = Depends(get_current_task),
    db: Session = Depends(get_db),
) -> None:

    task_service.delete_task(
    db,
    current_task.id,
)
    