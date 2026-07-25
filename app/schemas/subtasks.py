from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SubtaskBase(BaseModel):
    title: str


class SubtaskCreate(SubtaskBase):
    pass


class SubtaskUpdate(BaseModel):
    title: str | None = None
    is_completed: bool | None = None


class SubtaskResponse(SubtaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    is_completed: bool
    created_at: datetime
    updated_at: datetime