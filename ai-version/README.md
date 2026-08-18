# 📋 Task API — FastAPI In-Memory CRUD

A lightweight To-Do list API built with **FastAPI**. All data lives in memory (no database). Supports full **CRUD** operations, filtering, statistics, and a reset endpoint.

---

## 🚀 Quick Start

### 1. Clone / navigate to the project

```bash
cd ai-version
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

```bash
# Linux / macOS
source venv/bin/activate

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the server (one command)

```bash
python main.py
```

The server starts at **http://localhost:8000**.

> Alternatively you can use: `uvicorn main:app --reload`

---

## 📖 Swagger UI

Once the server is running, open your browser and navigate to:

| UI | URL |
|---|---|
| **Swagger (interactive)** | [http://localhost:8000/docs](http://localhost:8000/docs) |
| **ReDoc (read-only)** | [http://localhost:8000/redoc](http://localhost:8000/redoc) |

You can test every endpoint directly from the Swagger UI.

---

## 📡 API Endpoints

### General

| Method | Path | Description | Status |
|--------|------|-------------|--------|
| `GET` | `/` | API metadata (name, version, endpoints) | `200` |
| `GET` | `/health` | Health check — returns `{"status": "ok"}` | `200` |

### Tasks — CRUD

| Method | Path | Description | Status |
|--------|------|-------------|--------|
| `GET` | `/tasks` | List all tasks | `200` |
| `GET` | `/tasks/{task_id}` | Get a single task by ID | `200` / `404` |
| `POST` | `/tasks` | Create a new task (body: `{"title": "..."}`) | `201` / `400` |
| `PUT` | `/tasks/{task_id}` | Update a task (body: `{"title": "...", "done": true}`) | `200` / `400` / `404` |
| `DELETE` | `/tasks/{task_id}` | Delete a task | `204` / `404` |

### Query & Stats

| Method | Path | Description | Status |
|--------|------|-------------|--------|
| `GET` | `/tasks/search?title=...&done=...` | Filter tasks by title substring and/or done status | `200` |
| `GET` | `/tasks/stats` | Get counts: total, done, open | `200` |
| `POST` | `/tasks/reset` | Restore the 3 default example tasks | `200` |

---

## 🔢 Status Codes

| Code | Meaning |
|------|---------|
| `200` | Successful read / update |
| `201` | Resource created |
| `204` | Resource deleted (no content) |
| `400` | Invalid request body (missing/empty title, no fields to update) |
| `404` | Task with the given ID not found |
| `422` | Validation error (automatic from FastAPI/Pydantic) |

---

## 🗂 Project Structure

```
ai-version/
├── main.py              # FastAPI application (all endpoints)
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── venv/                # Virtual environment (not committed)
```

---

## 📝 Example Requests

### Create a task

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries"}'
```

### Update a task

```bash
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'
```

### Delete a task

```bash
curl -X DELETE http://localhost:8000/tasks/2
```

### Filter tasks

```bash
# By title keyword
curl "http://localhost:8000/tasks/search?title=api"

# By status
curl "http://localhost:8000/tasks/search?done=false"

# Combined
curl "http://localhost:8000/tasks/search?title=api&done=false"
```

### Reset to defaults

```bash
curl -X POST http://localhost:8000/tasks/reset
```

---

## 🛠 Tech Stack

- **Python 3.12+**
- **FastAPI** — modern async web framework
- **Pydantic** — data validation
- **Uvicorn** — ASGI server

---

## 📄 License

This project is for educational / demonstration purposes.
