# Task API

A simple REST API built with FastAPI as part of the FlyRank Backend AI Engineering Internship.

## Prerequisites

- Python 3.x
- FastAPI
- Uvicorn

## Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd task-api
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the server

```bash
uvicorn main:app --reload
```

The server will start at:

```
http://localhost:8000
```

## Test

Open in your browser:

```
http://localhost:8000/
```

Or use:

```bash
curl.exe -i http://localhost:8000/
```

Swagger documentation:

```
http://localhost:8000/docs
```

## Current Progress

- ✅ Stage 0: Hello Server
- ✅ Stage 1: Root and Health Endpoints
- ✅ Stage 2: read endpoint with 404
- ✅ Stage 3: created with validation
- ✅ Stage 4: Full CRUD