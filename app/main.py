from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, health, subtasks, tasks
from app.ai_agent.router import router as ai_router


app = FastAPI(
    title="TaskFlow API",
    description="Task and project management API",
    version="0.1.0",
)

origins = [
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health.router)
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(subtasks.router)
app.include_router(ai_router)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "TaskFlow API is running",
    }