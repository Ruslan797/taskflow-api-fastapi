from sqlalchemy.orm import Session

from app.services import task_service


def get_tasks_tool(
    db: Session,
    user_id: int,
):
    tasks = task_service.get_tasks(
        db,
        user_id,
    )

    return tasks