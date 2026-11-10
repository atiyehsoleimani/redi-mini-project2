from datetime import datetime, timezone
from app.models import Task, TaskCreate
from app.models import TaskUpdate

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


def list_tasks(status=None, priority=None, tag=None, search=None) -> list[Task]:
    tasks = list(_tasks.values())

    if status is not None:
        tasks = [task for task in tasks if task.status == status]
    if priority is not None:
        tasks = [task for task in tasks if task.priority == priority]
    if tag is not None:
        tasks = [task for task in tasks if tag in task.tags]
    if search is not None:
        text = search.lower()
        tasks = [
            task for task in tasks
            if text in task.title.lower() or text in (task.description or "").lower()
        ]
    return tasks


def update_task(task_id: int, task_in: TaskUpdate) -> Task | None:
    if task_id not in _tasks:
        return None
    task = _tasks[task_id]
    changes = task_in.model_dump(exclude_unset=True)
    updated = task.model_copy(update=changes)
    _tasks[task_id] = updated
    return updated


def delete_task(task_id: int) -> bool:
    if task_id in _tasks:
        _tasks.pop(task_id)
        return True
    return False

