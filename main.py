from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, Field
from typing import Annotated
class TaskCreate(BaseModel):
    title: str | None = None
class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None
app = FastAPI(
    title="Task API",
    description="A simple CRUD API built with FastAPI for the FlyRank Backend AI Engineering Internship.",
    version="1.0.0"
)
tasks = [
    { "id": 1, "title": "Prayer", "done": False},
    { "id": 2, "title": "Deep Work", "done": False},
    { "id": 3, "title": "Exercise", "done": False}
    ]
@app.get("/", summary="Returns information about the Task API")
async def root():
    return { 
        "name":  "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
        }
@app.get("/health", summary="Checks whether the API is running")
async def health():
    return {
        "status": "ok"
    }
@app.get("/stats", summary = "Return task statistics")
async def get_stats():
    total_tasks = len(tasks)
    done_task = sum(1 for task in tasks if task["done"] is True)
    open_tasks = total_tasks - done_task
    return{
        "total":total_tasks,
        "done":done_task,
        "open":open_tasks
    }
@app.post("/reset", summary = "reset all tasks")
async def reset_tasks():
    tasks.clear()
    tasks.extend([
        { "id": 1, "title": "Prayer", "done": False},
        { "id": 2, "title": "Deep Work", "done": False},
        { "id": 3, "title": "Exercise", "done": False}
        ])
    return tasks

@app.get("/tasks",summary="Returns all tasks")
async def get_tasks(done : bool | None = None, search: str | None = None):
    clear_search = search.strip().lower() if search else ""
    if done is None and search is None:
        return tasks
    elif search is None and done is not None:
        return [task for task in tasks if task["done"] == done]
    elif done is None and search is not None:
        return [task for task in tasks if clear_search in task["title"].lower()]
    return [task for task in tasks if task["done"] == done and clear_search in task["title"].lower()]
@app.get("/tasks/{task_id}", summary="Returns a task by its ID")
async def task_by_id(task_id: int):
    for task in tasks:
        if  task["id"] == task_id:
            return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error":f"Task {task_id} not found"}
    )
@app.post("/tasks", status_code=status.HTTP_201_CREATED, summary="Create a new Task")
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
@app.put("/tasks/{task_id}",summary="Updates an existing task")
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
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Deletes a task")
async def delete_task(task_id:int):
    for index,task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error": f"Task {task_id} not found"}
    )

