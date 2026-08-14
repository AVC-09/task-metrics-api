# Task & Metrics API (FastAPI + Redis)

A lightweight, production-ready RESTful API built with **FastAPI** and **Redis**. Fully containerized with **Docker**, deployable to **Kubernetes** (locally via **Kind** or **Helm**), and automated with **GitHub Actions CI**.

---

## 🏗️ Architecture & Stack

```text
               +-------------------------------------------------------+
               |                  GitHub Actions CI                    |
               |       (Lint Helm Chart & Build Docker Image)          |
               +-------------------------------------------------------+
                                           │
                                           ▼
                                [ Local Dev / Kind ]
                               http://localhost:8000
                                         │
                                         ▼
+---------------------------------------------------------------------------------+
| Kubernetes Cluster (dev-cluster)                                                |
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
|                               | PersistentVolume   |                            |
|                               | Claim (redis-pvc)  |                            |
|                               +--------------------+                            |
+---------------------------------------------------------------------------------+
```

---

## ✨ Features

- **Metrics & Persistence:** Total visit counter persisted in Redis across container restarts.
- **Task Management:** REST endpoints to create, retrieve, and list task IDs.
- **Input Validation:** Pydantic models preventing empty or whitespace-only titles.
- **Multi-Stage Docker Build:** Optimized image footprint using `python:3.11-slim`.
- **Helm Package Management:** Templated K8s manifests for multi-environment deployments (`helm/`).
- **CI/CD Automation:** GitHub Actions workflow (`ci.yml`) validating Helm syntax and Docker build status on every push.

---

## 🛠️ Tech Stack

* **Language & Framework:** Python 3.11 / FastAPI / Uvicorn
* **Database:** Redis 7 (In-Memory & Persistent)
* **Containerization:** Docker & Multi-stage builds
* **Orchestration:** Docker Compose / Kubernetes (Kind) / Helm v3
* **CI/CD:** GitHub Actions

---

## 🚀 Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/) with WSL 2 integration
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [kind](https://kind.sigs.k8s.io/)
- [helm](https://helm.sh/docs/intro/install/)

### 1. Clone the repository
```bash
git clone [https://github.com/AVC-09/task-metrics-api.git](https://github.com/AVC-09/task-metrics-api.git)
cd task-metrics-api
```

### 2. Deploy with Helm (Recommended)

1. **Create the Kind cluster:**
   ```bash
   kind create cluster --name dev-cluster --config k8s/kind-config.yaml
   ```

2. **Build and load the Docker image into Kind:**
   ```bash
   docker build -t task-api:v1 .
   kind load docker-image task-api:v1 --name dev-cluster
   ```

3. **Install the Helm Chart:**
   ```bash
   helm install my-app ./helm/task-metrics-app
   ```

4. **Verify deployment:**
   ```bash
   kubectl get pods
   helm list
   ```

---

## 🐳 Alternative Deployment Options

<details>
<summary><b>Option A: Deploy using Raw Kubernetes Manifests</b></summary>

```bash
kubectl apply -f k8s/redis.yaml
kubectl apply -f k8s/api.yaml
```
</details>

<details>
<summary><b>Option B: Run with Docker Compose</b></summary>

```bash
docker compose up -d
```
</details>

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Returns API status and total visit metrics |
| `POST` | `/tasks/` | Creates a new task (Validates non-empty title) |
| `GET` | `/tasks/` | Lists all existing Task IDs and total count |
| `GET` | `/tasks/{task_id}` | Retrieves detailed information of a specific task |

---

## 🔄 CI/CD Pipeline

The repository includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that automatically triggers on every `push` or `pull_request` to:
1. Run syntax checks on the Helm Chart (`helm lint`).
2. Verify that the Docker image builds successfully without errors.

---

## 🧹 Cleanup

To uninstall the Helm release and destroy the local cluster:

```bash
helm uninstall my-app
kind delete cluster --name dev-cluster
```