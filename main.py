import os
import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Task & Metrics API")

# Connect to Redis using environment variables
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

class Task(BaseModel):
    title: str
    description: str = ""

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