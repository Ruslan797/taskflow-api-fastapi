from sqlalchemy.orm import Session

from app.services import task_service
from app.schemas import TaskCreate, TaskUpdate


def get_tasks_tool(
    db: Session,
    user_id: int,
):
    tasks = task_service.get_tasks(
        db,
        user_id,
    )

    return [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "project_id": task.project_id,
        }
        for task in tasks
    ]


def create_task_tool(
    db: Session,
    user_id: int,
    title: str,
    description: str | None = None,
):
    task_data = TaskCreate(
        title=title,
        description=description,
    )

    task = task_service.create_task(
        db=db,
        task_data=task_data,
        owner_id=user_id,
    )

    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "project_id": task.project_id,
    }


def update_task_tool(
    db: Session,
    user_id: int,
    task_id: int,
    title: str | None = None,
    description: str | None = None,
):
    task = task_service.get_task(
        db,
        task_id,
    )

    if task is None or task.owner_id != user_id:
        return {
            "error": "Task not found",
        }

    update_data = {}

    if title is not None:
        update_data["title"] = title

    if description is not None:
        update_data["description"] = description

    task_data = TaskUpdate(**update_data)

    updated_task = task_service.update_task(
        db,
        task_id,
        task_data,
    )

    return {
        "id": updated_task.id,
        "title": updated_task.title,
        "description": updated_task.description,
    }


def delete_task_tool(
    db: Session,
    user_id: int,
    task_id: int,
):
    task = task_service.get_task(
        db,
        task_id,
    )

    if task is None or task.owner_id != user_id:
        return {
            "error": "Task not found",
        }

    deleted = task_service.delete_task(
        db,
        task_id,
    )

    return {
        "success": deleted,
        "task_id": task_id,
    }