from datetime import datetime
from typing import Literal, Annotated
from pydantic import BaseModel, Field, StringConstraints


class TaskCreate(BaseModel):
    title: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    description: str | None = ""
    status: Literal["todo", "in_progress", "done"] = "todo"
    priority: Literal["low", "medium", "high"] = "medium"
    tags: list[str] = Field(default_factory=list)


class Task(TaskCreate):
    id: int
    created_at: datetime


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: Literal["todo", "in_progress", "done"] | None = None
    priority: Literal["low", "medium", "high"] | None = None
    tags: list[str] = Field(default_factory=list)
