from sqlalchemy.orm import Session
from src.models.folder_model import Folder, FolderCreate
from src.models.user_model import User
from fastapi import HTTPException

def get_folders_by_user(db: Session, user: User):
    folders = db.query(Folder).filter(Folder.user_id == user.id).all()
    if not folders:
        raise HTTPException(status_code=404, detail="Usuario sin contraseñas")
    return folders

def create_folder(db: Session, user: User, folder_data: FolderCreate):
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
    return {"message": f"Contraseña guardada: {new_folder.name}"}
