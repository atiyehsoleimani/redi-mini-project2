from fastapi import APIRouter, HTTPException
from app.models import Task, TaskCreate
from app.services import task_services

router = APIRouter(tags=["Tasks"])


@router.post("/tasks", status_code=201)
def create_task(task_in: TaskCreate) -> Task:
    return task_services.create_task(task_in)


@router.get("/tasks/{task_id}")
def get_task(task_id: int) -> Task:
    task = task_services.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id: {task_id} does not exist.")
    else:
        return task
