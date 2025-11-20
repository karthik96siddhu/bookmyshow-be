from typing import List, Optional, Union
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class TaskCreate(BaseModel):
    title: str
    description: Union[str, None] = None
    completed: bool = False

class Task(TaskCreate):
    id: int
    created_at: datetime
    
# in memory "DB"
_tasks: List[Task] = []
_next_id = 1

@app.get("/", tags=["health"])
def get_status():
    return {"status": 'ok'}

@app.get("/greet", tags=["health"])
def greet():
    return {"message": "Welcome to FastApi development"}

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(task_in: TaskCreate):
    global _next_id
    task = Task(
        id = _next_id,
        created_at = datetime.utcnow(),
        **task_in.dict()
    )
    _tasks.append(task)
    _next_id += 1
    return task

# list tasks with optional filtering
@app.get("/tasks", response_model=List[Task], tags=["tasks"])
def get_tasks(completed: Optional[bool] = None, q: Optional[str] = None):
    results = _tasks
    if completed is not None:
        results = [t for t in results if t.completed == completed]
    if q:
        q_lower = q.lower()
        results = [t for t in results if q_lower in t.title.lower() or (t.description and q_lower in t.description.lower())]
    return results

# Update task
@app.put("/tasks/{task_id}", response_model=Task, tags=["tasks"])
def update_task(task_id: int, task_in: TaskCreate):
    for idx, t in enumerate(_tasks):
        if t.id == task_id:
            updated = Task(id=t.id, created_at=t.created_at, **task_in.dict())
            _tasks[idx] = updated
            return updated
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

# Delete task
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: int):
    for idx, t in enumerate(_tasks):
        if t.id == task_id:
            _tasks.pop(idx)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")