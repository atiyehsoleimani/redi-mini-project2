# Task Manager API

Create tasks, Delete tasks, Search and Filter Tasks.

## Setup

```bash
git clone https://github.com/atiyehsoleimani/redi-mini-project2.git
cd redi-mini-project2
git checkout mini-project-2
uv sync
```

## Run

```bash
uv run uvicorn app.main:app --reload
```

- Web page: http://127.0.0.1:8000/
- API docs: http://127.0.0.1:8000/docs

## Tests

```bash
uv run pytest -q
```

## API

| Method | Path | What it does | Success code |
|---|---|---|---|
| POST | /tasks | Create a task | 201 |
| GET | /tasks | List tasks (filters below) | 200 |
| GET | /tasks/{id} | Get one task | 200, or 404 |
| PUT / PATCH | /tasks/{id} | Update a task | 200, or 404 |
| DELETE | /tasks/{id} | Delete a task | 204, or 404 |

Filters for `GET /tasks`: `status`, `priority`, `tag`, `search`.

POST /tasks
{
  "title": "string",
  "description": "",
  "status": "todo",
  "priority": "medium",
  "tags": [
    "string"
  ]
}

- Tasks are stored in memory and disappear when the server restarts.
