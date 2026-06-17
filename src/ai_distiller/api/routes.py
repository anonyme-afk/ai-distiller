"""
routes.py
FastAPI routes.
"""
from fastapi import APIRouter, WebSocket
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
def chat(req: ChatRequest):
    return {"response": f"Stub model response for: {req.message}"}

@router.post("/generate")
def generate(req: ChatRequest):
    return {"generated_text": "Stub generated text"}

@router.post("/distill")
def distill():
    return {"status": "started distillation background task"}

@router.get("/models")
def list_models():
    return {"models": ["distilled-support-client-v1"]}

@router.get("/status")
def status():
    return {"training_status": "idle"}

@router.websocket("/stream")
async def stream(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Streaming stub...")
    await websocket.close()
