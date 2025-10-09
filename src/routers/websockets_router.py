from fastapi import WebSocket
from fastapi import APIRouter, Depends
from src.models.user_model import User
from src.services import websocket_service
from src.services.auth_dependency import get_current_user

from src.services import websocket_service

ws_router = APIRouter()

@ws_router.get("", tags=["Websockets"])
def get_ws():
    return websocket_service.test()

@ws_router.websocket("/dashboard")
async def ws_dashboard(
        websocket: WebSocket,
        current_user: User = Depends(get_current_user)
    ):
    return await websocket_service.ws_dashboard(websocket, current_user.id)

@ws_router.websocket("/sidebar")
async def ws_sidebar(
        websocket: WebSocket,
        current_user: User = Depends(get_current_user)
    ):
    return await websocket_service.ws_sidebar(websocket, current_user.id)
