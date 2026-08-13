# Task & Metrics API (FastAPI + Redis)

A lightweight, production-ready RESTful API built with **FastAPI** and **Redis**. Fully containerized with **Docker**, orchestrated locally via **Docker Compose**, and deployable to **Kubernetes** using **Kind**.

---

## 🏗️ Architecture Overview

### Kubernetes Architecture (Kind)

```text
                               [ Windows / WSL 2 ]
                               http://localhost:8000
                                         │
                                         ▼
+---------------------------------------------------------------------------------+
| Kind Cluster (dev-cluster)                                                      |
|                                                                                 |
|   +-------------------------------------------------------------------------+   |
|   | Task API Service (NodePort: 30080 -> Port: 8000)                        |   |
|   +-------------------------------------------------------------------------+   |
|                                         │                                       |
|                                         ▼                                       |
|   +-------------------+       +--------------------+                            |
|   | Task API Pod      | ----> | Redis Service      | (ClusterIP: 6379)          |
|   | (task-api:v1)     |       | (DNS: redis)       |                            |
|   +-------------------+       +--------------------+                            |
|                                         │                                       |
|                                         ▼                                       |
|                               +--------------------+                            |
|                               | Redis Pod          |                            |
|                               | (redis:7-alpine)   |                            |
|                               +--------------------+                            |
|                                         │                                       |
|                                         ▼                                       |
|                               +--------------------+                            |
|                               | PersistentVolume   |                            |
|                               | Claim (redis-pvc)  |                            |
|                               +--------------------+                            |
+---------------------------------------------------------------------------------+
```


### Docker Compose Architecture (Alternatively)

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

- **Metrics & Persistence:** Total visit counter persisted in Redis across container restarts.
- **Task Management:** REST endpoints to create, retrieve, and list task IDs.
- **Input Validation:** Pydantic models preventing empty or whitespace-only titles.
- **Multi-Stage Docker Build:** Optimized image footprint using `python:3.11-slim`.
- **Dual Orchestration:** Run locally with either **Docker Compose** or **Kubernetes (Kind)**.

---

## 🚀 Getting Started with Kubernetes (Kind)

### Prerequisites

- [Docker Desktop](https://www.docker.com/) with WSL 2 integration
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [kind](https://kind.sigs.k8s.io/)

### Local Kubernetes Deployment
1. **Clone the repository:**
   ```bash
   git clone https://github.com/AVC-09/task-metrics-api.git
   cd task-metrics-api
   ```

2. **Create the Kind cluster:**
   ```bash
   kind create cluster --name dev-cluster --config k8s/kind-config.yaml
   ```

3. **Build and load the Docker image into Kind:**
   ```bash
   docker build -t task-api:v1 .
   kind load docker-image task-api:v1 --name dev-cluster
   ```

4. **Deploy Redis resources (PVC, Deployment, Service):**
   ```bash
   kubectl apply -f k8s/redis.yaml
   ```

5. **Deploy API resources (Deployment, NodePort Service):**
   ```bash
   kubectl apply -f k8s/api.yaml
   ```

6. **Verify deployment status:**
   ```bash
   kubectl get pods
   kubectl get svc
   ```

7. **Access the application:**
   - **Metrics Endpoint:** [http://localhost:8000/](http://localhost:8000/)
   - **Swagger Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🐳 Alternative: Running with Docker Compose

If you prefer to run using Docker Compose instead of Kubernetes:

```bash
# Start services
docker compose up -d

# Stop services and remove volumes
docker compose down -v
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Returns API status and total visit metrics |
| `POST` | `/tasks/` | Creates a new task (Validates non-empty title) |
| `GET` | `/tasks/` | Lists all existing Task IDs and total count |
| `GET` | `/tasks/{task_id}` | Retrieves detailed information of a specific task |

---

## 🧹 Kubernetes Cleanup

To tear down the Kubernetes resources or delete the cluster:

```bash
# Delete Kubernetes resources
kubectl delete -f k8s/api.yaml
kubectl delete -f k8s/redis.yaml

# Delete the Kind cluster
kind delete cluster --name dev-cluster
```