"""
server.py
FastAPI server implementation.
"""
from fastapi import FastAPI
from .routes import router

app = FastAPI(title="AI-Distiller API", description="API to use distilled models")

app.include_router(router)

@app.get("/")
def root():
    return {"status": "ok", "message": "Welcome to AI-Distiller API"}
