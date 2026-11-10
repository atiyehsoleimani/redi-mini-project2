from typing import Literal
from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.models import TaskCreate
from app.services import task_services
from pydantic import ValidationError

router = APIRouter(include_in_schema=False)

templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def home(request: Request, status: str | None = None, priority: str | None = None, tag: str | None = None, search: str | None = None):

    tasks = task_services.list_tasks(status=status or None, priority=priority or None, tag=tag or None, search=search or None)
    return templates.TemplateResponse(request=request, name="index.html", context={"tasks": tasks, "status": status, "priority": priority, "tag": tag, "search": search })


@router.post("/add-task")
def add_task(request: Request, title: str=Form(""), description: str=Form(""), status: str=Form(""), priority: str=Form(""), tags: str=Form("")):
    tags = [tag.strip() for tag in tags.split(",") if tag.strip()]
    try:
        task_create = TaskCreate(title=title, description=description,status=status or "todo", priority=priority or "medium", tags=tags)
    except ValidationError:
        return templates.TemplateResponse(
        request,
        "index.html",
        {
            "tasks": task_services.list_tasks(),
            "error": "The title cannot be empty.",
        },
        status_code=422,
    )
    else:
        task_services.create_task(task_create)
        return RedirectResponse("/", status_code=303)
