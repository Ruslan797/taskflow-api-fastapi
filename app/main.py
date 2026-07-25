from fastapi import FastAPI

from app.routers import health, subtasks, tasks


app = FastAPI(
    title="TaskFlow API",
    description="Task and project management API",
    version="0.1.0",
)


app.include_router(health.router)
app.include_router(tasks.router)
app.include_router(subtasks.router)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "TaskFlow API is running",
    }