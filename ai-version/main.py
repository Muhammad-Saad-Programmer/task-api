"""
Task API — A FastAPI-powered in-memory To-Do List CRUD application.

Provides full Create, Read, Update, Delete operations on tasks,
with filtering, statistics, and a reset endpoint.
"""

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import Optional


# ---------------------------------------------------------------------------
# Pydantic models for request / response validation
# ---------------------------------------------------------------------------

class TaskCreate(BaseModel):
    """Schema used when creating a new task. Only `title` is required."""
    title: str = Field(
        ...,
        min_length=1,
        description="Title of the task (cannot be empty)",
        json_schema_extra={"example": "Buy groceries"},
    )


class TaskUpdate(BaseModel):
    """Schema used when updating an existing task. Both fields are optional."""
    title: Optional[str] = Field(
        None,
        min_length=1,
        description="New title for the task",
        json_schema_extra={"example": "Buy organic groceries"},
    )
    done: Optional[bool] = Field(
        None,
        description="Mark the task as done or not done",
        json_schema_extra={"example": True},
    )


class TaskOut(BaseModel):
    """Schema returned to the client for a single task."""
    id: int
    title: str
    done: bool


class StatsOut(BaseModel):
    """Aggregate statistics about the task list."""
    total: int
    done: int
    open: int


class APIInfo(BaseModel):
    """Basic metadata about this API."""
    name: str
    version: str
    endpoints: list[str]


class HealthOut(BaseModel):
    """Health-check response."""
    status: str


class MessageOut(BaseModel):
    """Generic message response."""
    message: str


# ---------------------------------------------------------------------------
# Default seed data
# ---------------------------------------------------------------------------

def _default_tasks() -> list[dict]:
    """Return the three example tasks used on startup and after reset."""
    return [
        {"id": 1, "title": "Learn FastAPI",       "done": False},
        {"id": 2, "title": "Build a CRUD API",    "done": False},
        {"id": 3, "title": "Write documentation", "done": True},
    ]


# In-memory task store
tasks: list[dict] = _default_tasks()


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _next_id() -> int:
    """Generate the next sequential task id."""
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1


def _find_task(task_id: int) -> dict | None:
    """Look up a task by its id. Returns None when not found."""
    for t in tasks:
        if t["id"] == task_id:
            return t
    return None


# ---------------------------------------------------------------------------
# Application instance with Swagger metadata
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Task API",
    description=(
        "A lightweight in-memory To-Do list API built with **FastAPI**.\n\n"
        "Supports full **CRUD** operations, filtering, statistics, and a "
        "reset endpoint to restore default data.\n\n"
        "### Features\n"
        "- ✅ Create, Read, Update & Delete tasks\n"
        "- 🔍 Filter tasks by title keyword and completion status\n"
        "- 📊 View aggregate statistics\n"
        "- 🔄 Reset to default seed data\n"
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "General",
            "description": "API metadata and health checks.",
        },
        {
            "name": "Tasks",
            "description": "Full CRUD operations on the task list.",
        },
        {
            "name": "Query & Stats",
            "description": "Filtering and aggregate statistics for tasks.",
        },
    ],
)


# =====================================================================
# GENERAL ENDPOINTS
# =====================================================================

@app.get(
    "/",
    response_model=APIInfo,
    tags=["General"],
    summary="API Information",
    description="Returns basic metadata about the Task API including its name, version, and available endpoint groups.",
)
def get_api_info():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"],
    }


@app.get(
    "/health",
    response_model=HealthOut,
    tags=["General"],
    summary="Health Check",
    description="Simple liveness probe — returns `ok` when the server is running.",
)
def health_check():
    return {"status": "ok"}


# =====================================================================
# TASKS — READ
# =====================================================================

@app.get(
    "/tasks",
    response_model=list[TaskOut],
    tags=["Tasks"],
    summary="List All Tasks",
    description="Retrieve every task currently stored in memory.",
)
def get_all_tasks():
    return tasks


@app.get(
    "/tasks/search",
    response_model=list[TaskOut],
    tags=["Query & Stats"],
    summary="Search / Filter Tasks",
    description=(
        "Filter tasks by a **title** keyword (case-insensitive substring match) "
        "and/or by **done** status. Both query parameters are optional — omit "
        "them to return all tasks."
    ),
)
def search_tasks(
    title: Optional[str] = Query(
        None,
        description="Case-insensitive substring to search for in the task title",
        json_schema_extra={"example": "api"},
    ),
    done: Optional[bool] = Query(
        None,
        description="Filter by completion status (true = done, false = open)",
    ),
):
    results = tasks
    if title is not None:
        results = [t for t in results if title.lower() in t["title"].lower()]
    if done is not None:
        results = [t for t in results if t["done"] is done]
    return results


@app.get(
    "/tasks/stats",
    response_model=StatsOut,
    tags=["Query & Stats"],
    summary="Task Statistics",
    description="Returns aggregate counts: total tasks, completed tasks, and open tasks.",
)
def get_task_stats():
    total = len(tasks)
    done_count = sum(1 for t in tasks if t["done"])
    return {"total": total, "done": done_count, "open": total - done_count}


@app.get(
    "/tasks/{task_id}",
    response_model=TaskOut,
    tags=["Tasks"],
    summary="Get Task by ID",
    description="Retrieve a single task by its numeric ID. Returns 404 if the task does not exist.",
    responses={404: {"description": "Task not found"}},
)
def get_task_by_id(task_id: int):
    task = _find_task(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    return task


# =====================================================================
# TASKS — CREATE
# =====================================================================

@app.post(
    "/tasks",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Tasks"],
    summary="Create a New Task",
    description=(
        "Create a new task. Only `title` is required in the request body. "
        "The `id` is auto-generated and `done` defaults to `false`. "
        "Returns 400 if the title is missing or empty."
    ),
    responses={400: {"description": "Invalid request body (missing or empty title)"}},
)
def create_task(payload: TaskCreate):
    new_task = {
        "id": _next_id(),
        "title": payload.title.strip(),
        "done": False,
    }
    tasks.append(new_task)
    return new_task


# =====================================================================
# TASKS — UPDATE
# =====================================================================

@app.put(
    "/tasks/{task_id}",
    response_model=TaskOut,
    tags=["Tasks"],
    summary="Update an Existing Task",
    description=(
        "Update the `title` and/or `done` status of an existing task. "
        "At least one field must be provided. Returns 404 if the task "
        "does not exist, or 400 if the body is empty / invalid."
    ),
    responses={
        400: {"description": "No valid fields provided for update"},
        404: {"description": "Task not found"},
    },
)
def update_task(task_id: int, payload: TaskUpdate):
    task = _find_task(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )

    # Ensure at least one field is being updated
    if payload.title is None and payload.done is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request body must include at least 'title' or 'done'",
        )

    if payload.title is not None:
        task["title"] = payload.title.strip()
    if payload.done is not None:
        task["done"] = payload.done

    return task


# =====================================================================
# TASKS — DELETE
# =====================================================================

@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Tasks"],
    summary="Delete a Task",
    description="Permanently remove a task by its ID. Returns 204 on success or 404 if the task does not exist.",
    responses={404: {"description": "Task not found"}},
)
def delete_task(task_id: int):
    task = _find_task(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    tasks.remove(task)
    return None  # 204 — no content


# =====================================================================
# RESET
# =====================================================================

@app.post(
    "/tasks/reset",
    response_model=MessageOut,
    tags=["Query & Stats"],
    summary="Reset Tasks to Defaults",
    description=(
        "Wipe the current task list and restore the three default example tasks. "
        "Useful for testing and demos."
    ),
)
def reset_tasks():
    global tasks
    tasks = _default_tasks()
    return {"message": "Task list has been reset to default tasks"}


# ---------------------------------------------------------------------------
# Entry point — allows `python main.py` to start the server
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
