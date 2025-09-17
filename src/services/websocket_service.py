from fastapi import WebSocket, WebSocketDisconnect

from src.services.ws_manager import manager, sidebar_manager

def test():
    return {"message": "Hola ws"}


async def ws_dashboard(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Mensaje recibido: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

async def ws_sidebar(websocket: WebSocket):
    await sidebar_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Mensaje recibido: {data}")
    except WebSocketDisconnect:
        sidebar_manager.disconnect(websocket)