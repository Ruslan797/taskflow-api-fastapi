## Get Task by ID

The repository executes the database query:

```python
def get_task_by_id(
    db: Session,
    task_id: int,
) -> Task | None:
    statement = select(Task).where(Task.id == task_id)

    return db.scalar(statement)
```

!!! info "What happens here?"
    `select(Task)` creates a SQLAlchemy SELECT statement.

    At this moment PostgreSQL has not necessarily received
    the query yet.

    `db.scalar(statement)` executes the statement through
    the current SQLAlchemy Session.