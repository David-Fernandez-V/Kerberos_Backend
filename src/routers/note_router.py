from typing import List
from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from src.models.folder_model import FolderRequest
from src.database.db import get_db
from src.models.note_model import NoteCreate, NoteDetail, NoteOut, NoteRequest
from src.models.user_model import User
from src.services import note_service
from src.services.auth_dependency import get_current_user

note_router = APIRouter()

@note_router.post("/create", tags=["Notes"])
def create_note(
        note_data: NoteCreate ,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
    return note_service.create_note(db, note_data, current_user)

@note_router.post("/by-user", response_model=List[NoteOut], tags=["Notes"])
def get_notes(
    request: FolderRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return note_service.get_notes_by_user(db, current_user, request)

@note_router.post("/get_detail", response_model=NoteDetail, tags=["Notes"])
def get_note_detail(
    note_request: NoteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return note_service.get_note_detail(db, current_user, note_request)

@note_router.delete("/delete", tags=["Notes"])
def delete_note(
    note_request: NoteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return note_service.delete_note(db, current_user, note_request)