import json
import os
import sys
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="CS50P todo API")

DB_FILE = "todos.json"

class Todo(BaseModel):
    id: int
    task: str
    completed: bool = False

class TodoCreate(BaseModel):
    task: str

def load_data() -> list[dict]:
    if not os.path.exists(DB_FILE):
        return[]
    with open(DB_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []
def save_data(data: list[dict]):
    with open(DB_FILE, "w")as f:
        json.dump(data, f, indent=4)

def add_task(current_todos: list[dict], task_name: str) -> dict:
    if not task_name.strip():
        raise ValueError("Task name cannot be empty")
    
    new_id = max([t["id"] for t in current_todos], default=0) +1
    new_todo = {"id": new_id, "task": task_name, "completed": False}
    current_todos.append(new_todo)
    return new_todo
def updated_status(current_todos: list[dict], todo_id: int) -> Optional [dict]:
    for todo in current_todos:
        if todo["id"] == todo_id:
            todo["completed"] = not todo["completed"]
            return todo
    return None

def remove_task(current_todos: list[dict], todo_id: int) -> bool:
    for i, todo in enumerate(current_todos):
        if todo["id"] == todo_id:
            current_todos.pop(i)
            return True
    return False

@app.get("/todos")
def list_todos():
    return load_data()

@app.post("/todos", status_code=201)
def create_todo(todo: TodoCreate):
    data = load_data()
    try:
        new_item = add_task(data, todo.task)
        save_data(data)
        return new_item
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.put("/todos/{todo_id}")
def toggle_todo(todo_id: int):
    data = load_data()
    updated = updated_status(data, todo_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    save_data(data)
    return updated


@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    data = load_data()
    for todo in data:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    data = load_data()
    success = remove_task(data, todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    save_data(data)
    return {"detail": "Successfully deleted"}

def main():
    uvicorn.run(app, host="127.0.0.1",port=8000)

if __name__ == "__main__":
    main()
    