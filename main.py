import os
import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="Task & Metrics API")

# Connect to Redis using environment variables
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_SSL = os.getenv("REDIS_SSL", "false").lower() == "true"

db = redis.Redis(
    host=REDIS_HOST, 
    port=REDIS_PORT, 
    ssl=REDIS_SSL, 
    decode_responses=True,
    socket_timeout=3.0 # Prevents API requests from hanging indefinitely
)

class Task(BaseModel):
    title: str = Field(..., min_length=1, description="Task title cannot be empty")
    description: str = ""

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str) -> str:
        """Ensures title contains actual text and not just whitespace"""
        stripped_value = value.strip()
        if not stripped_value:
            raise ValueError("Title cannot be empty or blank spaces")
        return stripped_value

# Dedicated Health Check endpoint for Kubernetes Probes
@app.get("/healthz")
def health_check():
    """Liveness & Readiness probe endpoint for Kubernetes"""
    try:
        if db.ping():
            return {"status": "ok", "redis": "connected"}
        raise HTTPException(status_code=503, detail="Redis ping failed")
    except redis.ConnectionError:
        raise HTTPException(status_code=503, detail="Database connection error")

@app.get("/")
def read_root():
    """Visit counter to test persistence and metrics"""
    try:
        visits = db.incr("total_visits")
        return {
            "message": "Task & Metrics API running!",
            "total_visits": visits
        }
    except redis.ConnectionError:
        return {"message": "API running, but Redis is not connected yet!"}

@app.post("/tasks/")
def create_task(task: Task):
    """Saves a new task to Redis"""
    try:
        task_id = db.incr("task_id_counter")
        db.hset(f"task:{task_id}", mapping={"title": task.title, "description": task.description})
        return {"id": task_id, "title": task.title, "description": task.description}
    except redis.ConnectionError:
        raise HTTPException(status_code=500, detail="Database connection error")

@app.get("/tasks/")
def list_task_ids():
    """Retrieves a list of all existing Task IDs using non-blocking SCAN"""
    try:
        # SCAN instead of KEYS to avoid blocking the Redis event loop
        task_ids = sorted([
            int(key.split(":")[1]) 
            for key in db.scan_iter("task:*") 
            if key.split(":")[1].isdigit()
        ])
        return {"task_ids": task_ids, "count": len(task_ids)}
    except redis.ConnectionError:
        raise HTTPException(status_code=500, detail="Database connection error")

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Retrieves a task by its ID"""
    try:
        task = db.hgetall(f"task:{task_id}")
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"id": task_id, **task}
    except redis.ConnectionError:
        raise HTTPException(status_code=500, detail="Database connection error")