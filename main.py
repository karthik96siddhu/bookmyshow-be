from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    id: int
    title: str
    description: Union[str, None] = None
    completed: bool = False

@app.get("/")
def get_status():
    return {"status": "ok"}

@app.get("/greet")
def greet():
    return {"message": "Welcome to FastApi development"}

@app.post("/tasks")
def create_task(task: Task):
    return {"message": "Task created successfully", "task": task}

@app.get("/tasks")
def get_tasks():
    tasks = [
        {"id": 1, "title": "Sample Task", "description": "This is a sample task", "completed": False},
        {"id": 2, "title": "Another Task", "description": "This is another task", "completed": True}
    ]
    return {"tasks": tasks}