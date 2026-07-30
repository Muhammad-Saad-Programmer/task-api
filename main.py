from fastapi import FastAPI, HTTPException, status
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
        detail=f"Task {task_id} not found"
    )

    
