from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .agent_service import get_ai_response
import json

router = APIRouter()

# Input model
class TaskRequest(BaseModel):
    task: str
    mode: str = "autonomous"

@router.post("/agent/process")
def process_agent(request: TaskRequest):
    task_text = request.task
    mode = request.mode

    try:
        response_str = get_ai_response(task_text, mode)
        # Try parsing JSON from the AI response
        response_json = json.loads(response_str)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="AI response is not valid JSON")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "mode": mode,
        "response": response_json
    }
