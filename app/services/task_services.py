from datetime import datetime, timezone
from app.models import Task, TaskCreate

_tasks: dict[int, Task] = {}
_next_id = 1


def create_task(task_in: TaskCreate) -> Task:
    global _next_id
    task = Task(**task_in.model_dump(), created_at=datetime.now(timezone.utc), id=_next_id)
    _tasks[_next_id] = task
    _next_id += 1
    return task


def get_task(task_id: int) -> Task | None:
    return _tasks.get(task_id)


def reset_tasks():
    global _next_id
    _tasks.clear()
    _next_id = 1
