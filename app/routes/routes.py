from fastapi import APIRouter, HTTPException
from app.models import Task, TaskCreate, TaskUpdate
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


@router.get("/tasks")
def list_tasks() -> list[Task]:
    return task_services.list_tasks()

@router.put("/tasks/{task_id}")
@router.patch("/tasks/{task_id}")
def update_task(task_id: int, task_in: TaskUpdate) -> Task:
    task = task_services.update_task(task_id, task_in)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id: {task_id} does not exist.")
    return task


@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int) -> None:
    if task_services.delete_task(task_id) is False:
        raise HTTPException(status_code=404, detail=f"Task with id: {task_id} does not exist." )
