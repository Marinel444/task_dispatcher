# Task Dispatcher — Automatic Task Assignment System

A lightweight Django REST Framework service for creating tasks, automatically assigning them to workers based on priority and workload, and providing system statistics. Includes a background worker, PostgreSQL support, fixtures, and Swagger documentation.

---

## 🚀 Features

- Create tasks via REST API  
- Update task status (`pending → in_progress → completed`)  
- Automatic assignment every 10 seconds  
- Load-balanced worker selection  
- Auto-scaling workers:  
  - queue > 10 → add worker  
  - queue < 5 → keep only 2 active workers  
- System statistics endpoint  
- Swagger documentation  

---

## 📚 API Documentation

**Swagger UI:**  
```
http://localhost:8000/api/swagger/
```

**OpenAPI schema:**  
```
http://localhost:8000/api/schema/
```

---

## 🧪 Main Endpoints

```
POST /api/tasks/                — create task
PATCH /api/tasks/<id>/status/   — update task status
GET /api/workers/               — list workers
GET /api/task-status/           — system statistics
```

---

## 📦 Running with Docker

### 1. Create `.env`

```
POSTGRES_DB=task_db
POSTGRES_USER=task_user
POSTGRES_PASSWORD=task_pass
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### 2. Start services

Run the project using Docker Compose:

```bash
  docker-compose up --build
```

### Services

| Service | Description |
|--------|-------------|
| web    | Django API server |
| worker | Background task dispatcher |
| db     | PostgreSQL |

---

## 🧩 Fixtures

Fixtures load automatically from:

```
initial_data.json
```

They include workers and test tasks for demonstration.

---

## ✔ Project Status

Fully functional and ready for evaluation:  
REST API, automatic task distribution, background worker, Docker environment, fixtures, and Swagger UI.