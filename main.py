from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
class TaskCreate(BaseModel):
    title: str | None = None
app = FastAPI()
tasks = [
    { "id": 1, "title": "Prayer", "done": False},
    { "id": 2, "title": "Deep Work", "done": False},
    { "id": 3, "title": "Exercise", "done": False}
    ]
@app.get("/")
async def root():
    return { 
        "name":  "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
        }
@app.get("/health")
async def health():
    return {
        "status": "ok"
    }
@app.get("/tasks")
async def get_tasks():
    return tasks
@app.get("/tasks/{task_id}")
async def task_by_id(task_id: int):
    for task in tasks:
        if  task["id"] == task_id:
            return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error":f"Task {task_id} not found"}
    )
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(task_data: TaskCreate):
    if not task_data.title or task_data.title.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Title is required and cannot be empty"}
        )
    next_id = max([t["id"] for t in tasks], default = 0) + 1
    new_task = {
        "id": next_id,
        "title": task_data.title.strip(),
        "done": False
    }
    tasks.append(new_task)
    return new_task

    
