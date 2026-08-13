# Task & Metrics API (FastAPI + Redis)

A lightweight, production-ready RESTful API built with **FastAPI** and **Redis**, fully containerized using **Docker** and orchestrated with **Docker Compose**. Designed with DevOps best practices, including multi-stage image builds, environment variable configuration, input validation, and volume persistence.

---

## 🏗️ Architecture Overview

```text
               +-------------------------------------------+
               |              Docker Network               |
               |               (app-network)               |
               |                                           |
Client Request |   +-----------------+   +-------------+   |
 ------------->|   |  FastAPI (API)  |-->| Redis (DB)  |   |
  (Port 8000)  |   |  Container      |   | Container   |   |
               |   +-----------------+   +-------------+   |
               +--------------------------------|----------+
                                                v
                                       +------------------+
                                       | Named Volume     |
                                       | (redis-data)     |
                                       +------------------+
```

---

## ✨ Features

- **Visit Counter & Metrics:** Tracks overall endpoint hits persisted in Redis.
- **Task Management:** REST endpoints to create, list, and fetch tasks by ID.
- **Input Validation:** Strict data models powered by Pydantic (prevents empty/blank task titles).
- **Multi-Stage Dockerfile:** Optimized runtime image size using `python:3.11-slim`.
- **Data Persistence:** Uses Docker named volumes to prevent data loss upon container termination.
- **Auto-Generated Docs:** Swagger UI available natively at `/docs`.

---

## 🛠️ Tech Stack

* **Language:** Python 3.11
* **Framework:** FastAPI / Uvicorn
* **Database:** Redis 7 (In-memory & Persistent Snapshotting)
* **Containerization:** Docker & Docker Compose
* **Validation:** Pydantic v2

---

## 🚀 Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (includes Docker Compose)
- [Git](https://git-scm.com/)

### Installation & Execution

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AVC-09/task-metrics-api.git
   cd task-metrics-api
   ```

2. **Start the application stack:**
   ```bash
   docker compose up -d
   ```

3. **Verify running containers:**
   ```bash
   docker compose ps
   ```

4. **Access the API:**
   - **Metrics Endpoint:** [http://localhost:8000/](http://localhost:8000/)
   - **Interactive API Docs (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Returns API status and total visit metrics |
| `POST` | `/tasks/` | Creates a new task (Validates non-empty title) |
| `GET` | `/tasks/` | Lists all existing Task IDs and total count |
| `GET` | `/tasks/{task_id}` | Retrieves detailed information of a specific task |

---

## 🧪 Testing Persistence

1. Create a few tasks via `/docs` or `curl`.
2. Stop and remove the containers:
   ```bash
   docker compose down
   ```
3. Restart the containers:
   ```bash
   docker compose up -d
   ```
4. Query `GET /` or `GET /tasks/`. Notice your visit count and created tasks remain intact thanks to the `redis-data` Docker volume.

---

## 🧹 Cleanup

To stop the services and remove networks/volumes:
```bash
docker compose down -v
```