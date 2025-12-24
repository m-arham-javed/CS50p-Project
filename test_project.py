import pytest
from project import add_task, updated_status, remove_task
from fastapi.testclient import TestClient
import project


def test_add_task():
    db = []
    item = add_task(db, "Test Task")
    assert item["task"] == "Test Task"
    assert item["id"] == 1
    assert len(db) == 1
    with pytest.raises(ValueError):
        add_task(db, "")

def test_updated_status():
    db =[{"id": 1, "task": "study", "completed": False}]
    updated = updated_status(db, 1)
    assert updated["completed"] is True
    assert updated_status(db, 99) is None

def test_remove_task():
    db = [{"id": 1, "task": "study", "completed": False}]
    success = remove_task(db, 1)
    assert success is True
    assert len(db) == 0
    assert remove_task (db, 99) is False


def test_get_todo_api(tmp_path, monkeypatch):
    # isolate test DB file
    db_file = tmp_path / "todos.json"
    monkeypatch.setattr(project, "DB_FILE", str(db_file))
    client = TestClient(project.app)

    # create a todo
    resp = client.post("/todos", json={"task": "Buy milk"})
    assert resp.status_code == 201
    item = resp.json()
    todo_id = item["id"]

    # get the created todo
    resp2 = client.get(f"/todos/{todo_id}")
    assert resp2.status_code == 200
    data = resp2.json()
    assert data["task"] == "Buy milk"

    # non-existent id -> 404
    resp3 = client.get("/todos/9999")
    assert resp3.status_code == 404
