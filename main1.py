from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import asyncio
import ollama
import anthropic

from modules.task.task_services import (
    add_task,
    get_tasks,
    update_task_status,
    delete_task
)
from modules.agent.agent_controller import router as agent_router

# -----------------------------
# Request Models
# -----------------------------
class TaskRequest(BaseModel):
    task: str
    mode: str = "autonomous"

class ChatRequest(BaseModel):
    message: str


class ProcessRequest(BaseModel):
    message: str
    task_id: Optional[int] = None
    context: Optional[str] = None
    priority: Optional[str] = None
    user_id: Optional[int] = None


class TaskCreateRequest(BaseModel):
    user_id: int
    task: str
    due_date: Optional[datetime] = None
    priority: Optional[str] = "medium"


class TaskUpdateRequest(BaseModel):
    task_id: int
    status: str


# -----------------------------
# App Initialization
# -----------------------------
app = FastAPI(title="Smart Agent Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent_router)

@app.on_event("startup")
async def warmup_model():
    try:
        await asyncio.to_thread(
            ollama.chat,
            model="llama3",
            messages=[{"role": "user", "content": "Hello"}],
            stream=False
        )
        print("Ollama model warmed up ✅")
    except Exception as e:
        print("Warmup failed:", e)

# -----------------------------
# Basic Route
# -----------------------------
@app.get("/")
async def home():
    return {"message": "Smart Agent Backend is Running!"}

# -----------------------------
# AI & Chat Endpoints
# -----------------------------
@app.post("/chat")
async def chat_endpoint(payload: ChatRequest):
    return {"reply": f"Agent processed: {payload.message}"}


@app.post("/process")
async def process_ai_task(payload: ProcessRequest):
    try:
        # Add timeout protection
        response = ollama.chat(
            model="llama3",
            messages=[
                {"role": "system", "content": "You are a smart task assistant."},
                {"role": "user", "content": payload.message}
            ],
            stream=False  # important for non-interactive)
        )

        ai_output = response["message"]["content"]
        return {"response": ai_output}

    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="AI request timed out")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# Task Management Endpoints
# -----------------------------
@app.post("/add_task")
async def create_new_task(payload: TaskCreateRequest):
    try:
        await asyncio.to_thread(
            add_task,
            payload.user_id,
            payload.task,
            payload.due_date.strftime("%Y-%m-%d") if payload.due_date else None,
            payload.priority or "medium",
        )
        return {"message": "Task added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/delete_task/{task_id}")
async def remove_task(task_id: int):
    delete_task(task_id)
    return {"message": f"Task {task_id} deleted successfully"}


@app.get("/tasks")
async def list_all_tasks():
    task_list = get_tasks()
    return {"tasks": [dict(t) for t in task_list]}
