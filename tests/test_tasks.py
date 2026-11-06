
def make_task(client, **fields):
    data = {}
    data.update(fields) 
    return client.post("/tasks", json=data)


# ----------------------------- create a task ---------------------------------


def test_create_task(client):
    response = make_task(client, title="Buy milk", status="in_progress", priority="high")

    assert response.status_code == 201

    task = response.json()
    assert task["id"] == 1
    assert task["title"] == "Buy milk"
    assert task["status"] == "in_progress"
    assert task["priority"] == "high"
    assert task["description"] == ""
    assert task["tags"] == []
    assert "created_at" in task


def test_ids_go_up(client):
    first = make_task(client, title="First")
    second = make_task(client, title="Second")

    assert first.json()["id"] == 1
    assert second.json()["id"] == 2


# ----------------------------- wrong data (422) ------------------------------


def test_missing_title(client):
    response = client.post("/tasks", json={"description": "no title"})

    assert response.status_code == 422


def test_empty_title(client):
    response = make_task(client, title="   ")  

    assert response.status_code == 422


def test_invalid_status(client):
    response = make_task(client, status="finished")  # not todo/in_progress/done

    assert response.status_code == 422


# ----------------------------- get one task ----------------------------------


def test_get_task(client):
    make_task(client, title="Read a book")

    response = client.get("/tasks/1")

    assert response.status_code == 200
    assert response.json()["title"] == "Read a book"


def test_get_task_not_found(client):
    response = client.get("/tasks/999")

    assert response.status_code == 404
