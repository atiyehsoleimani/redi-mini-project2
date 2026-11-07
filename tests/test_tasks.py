
def make_task(client, **fields):
    data = {}
    data.update(fields) 
    return client.post("/tasks", json=data)

def update_task(client, task_id, **fields):
    data={}
    data.update(fields)
    return client.patch(f"/tasks/{task_id}", json=data)
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
    make_task(client, title="Write an email")

    response = client.get("/tasks/1")

    assert response.status_code == 200
    assert response.json()["title"] == "Write an email"

def test_get_task_not_found(client):
    response = client.get("/tasks/999")

    assert response.status_code == 404

# ----------------------------- update one task --------------------------------

def test_update_task(client):
    assert make_task(client, title="Print a ticket", priority="low").status_code == 201
    response = update_task(client, 1,  priority="medium")

    assert response.json()["priority"] == "medium"

def test_update_with_invalid_status(client):
    assert make_task(client, title="Print a ticket", priority="low").status_code == 201
    response = update_task(client, 1, priority="urgent")
    assert response.status_code == 422

def test_update_not_found(client):
    response = update_task(client, 2,  priority="medium") 
    assert response.status_code == 404

#----------------------------- delete one task ---------------------------------

def test_delete_task(client):

    assert make_task(client, title="task to delete", priority="low").status_code == 201

    response = client.delete("/tasks/1")
    assert response.status_code == 204
    assert client.get("/tasks/1").status_code == 404

def test_delete_not_found(client):
    response = client.delete("/tasks/1")
    assert response.status_code == 404

def test_not_repeated_id_after_delete(client):
     assert make_task(client, title="task to delete", priority="low").status_code == 201
     client.delete("/tasks/1")

     assert make_task(client, title="task with id=2", priority="low").status_code == 201
     assert client.get("/tasks/2").json()["id"] == 2

#----------------------------- list tasks ---------------------------------
def test_list_tasks(client):
    assert make_task(client, title="first task", priority="low").status_code == 201
    assert make_task(client, title="second task", priority="low").status_code == 201

    response = client.get("/tasks")
    #assert response.lenght() == 2