from typing import List
from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.models.user_model import User
from src.services import folder_service
from src.services.auth_dependency import get_current_user
from src.models.folder_model import FolderOut, FolderCreate, FolderRequest

folder_router = APIRouter()

@folder_router.post("/by-user", response_model=List[FolderOut], tags=["Folders"])
def get_folders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return folder_service.get_folders_by_user(db, current_user)

@folder_router.post("/create", tags=["Folders"])
async def create_folders(
    folder_data: FolderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await folder_service.create_folder(db, current_user, folder_data)

@folder_router.delete("/delete", tags=["Folders"])
async def delete_folder(
    folder_request: FolderRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await folder_service.delete_folder(db, current_user, folder_request)