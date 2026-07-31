from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
class TaskCreate(BaseModel):
    title: str | None = None
class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None
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
            status_code=status.HTTP_400_BAD_REQUEST,
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
@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task_data: TaskUpdate):
    if task_data.title is None and task_data.done is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "At Least one Field (title or done) must be provided"}
        )
    if task_data.title is not None and task_data.title.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Title cannot be empty"}
        )
    for task in tasks:
        if task["id"] == task_id:
            if task_data.title is not None:
                task["title"] = task_data.title.strip()
            if task_data.done is not None:
                task["done"] = task_data.done
            return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error": f"Task {task_id} not found"}
    )
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id:int):
    for index,task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error": f"Task {task_id} not found"}
    )

