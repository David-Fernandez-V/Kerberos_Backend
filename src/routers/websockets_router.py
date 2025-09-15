from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi import APIRouter, Path, Depends
from sqlalchemy.orm import Session
from src.models.user_model import User
from src.database.db import get_db
from src.services import websocket_service
from src.services.auth_dependency import get_current_user
from src.services.ws_manager import manager

ws_router = APIRouter()

@ws_router.get("", tags=["Websockets"])
def get_ws():
    return websocket_service.test()

@ws_router.websocket("/dashboard")
async def ws_dashboard(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Mantener conexión
    except WebSocketDisconnect:
        manager.disconnect(websocket)
