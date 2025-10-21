import json
from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.models.folder_model import Folder, FolderCreate, FolderRequest
from src.models.user_model import User
from src.services.ws_manager import manager, sidebar_manager

def get_folders_by_user(db: Session, user: User):
    folders = db.query(Folder).filter(Folder.user_id == user.id).all()
    if not folders:
        raise HTTPException(status_code=404, detail="Usuario sin contraseñas")
    return folders

async def create_folder(db: Session, user: User, folder_data: FolderCreate):
    existing = db.query(Folder).filter(Folder.user_id == user.id, Folder.name == folder_data.name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Nombre no disponible")
    new_folder = Folder(
        user_id = user.id,
        name = folder_data.name,
    )
    db.add(new_folder)
    db.commit()
    db.refresh(new_folder)

    await sidebar_manager.send_to_user(user.id, json.dumps({
        "type": "folder",
    }))

    return {"message": f"Contraseña guardada: {new_folder.name}"}

async def modify_folder(db: Session, user: User, request: FolderRequest, new_data: FolderCreate):
    folder = db.query(Folder).filter(Folder.user_id == user.id, Folder.id == request.folder_id).first()
    if not folder:
        raise HTTPException(status=404, detail="Carpeta no encontrada")
    
    folder.name = new_data.name

    db.add(folder)
    db.commit()
    db.refresh(folder)

    await sidebar_manager.send_to_user(user.id, json.dumps({
        "type": "folder",
    }))

    await manager.send_to_user(user.id, json.dumps({
        "type": "note",
    }))

    await manager.send_to_user(user.id, json.dumps({
        "type": "password",
    }))

    await manager.send_to_user(user.id, json.dumps({
        "type": "card",
    }))

    return {"message": f"Carpeta modificada correctamente"}

async def delete_folder(db: Session, user: User, request: FolderRequest):
    folder = db.query(Folder).filter(Folder.user_id == user.id, Folder.id == request.folder_id).first()
    if not folder:
        raise HTTPException(status_code=404, detail="Carpeta no encontrada")
    
    db.delete(folder)
    db.commit()

    await sidebar_manager.send_to_user(user.id, json.dumps({
        "type": "folder",
    }))

    await manager.send_to_user(user.id, json.dumps({
        "type": "note",
    }))

    await manager.send_to_user(user.id, json.dumps({
        "type": "password",
    }))

    await manager.send_to_user(user.id, json.dumps({
        "type": "card",
    }))

    return {"message": f"Carpeta eliminada correctamente"}

