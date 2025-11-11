import json
import os
from sqlalchemy.orm import Session
from fastapi import HTTPException
from dotenv import load_dotenv
from cryptography.fernet import Fernet, InvalidToken
from passlib.context import CryptContext

from src.models.folder_model import FolderRequest
from src.models.note_model import Note, NoteDetail, NoteCreate, NoteRequest
from src.models.user_model import User
from src.services.ws_manager import manager

load_dotenv()
fernet = Fernet(os.getenv("ENCRYPTION_KEY").encode())

def decrypt_content(encrypted_content: str) -> str:
    return fernet.decrypt(encrypted_content.encode()).decode()

async def create_note(db: Session, note_data: NoteCreate, user: User):

    existing = db.query(Note).filter(Note.user_id == user.id,Note.title == note_data.title).first()
    if existing:
       raise HTTPException(status_code=409, detail="Titulo no disponible")
    
    content_encrypted = fernet.encrypt(note_data.content.encode()).decode()

    new_note = Note(
        user_id = user.id,
        title = note_data.title,
        content_encrypted = content_encrypted,
        ask_password = note_data.ask_master_password,
        folder_id = note_data.folder_id      
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    await manager.send_to_user(user.id, json.dumps({
        "type": "create_note",
    }))

    return {"message": f"Nota guardada: {new_note.title}"}
    
def get_notes_by_user(db: Session, user: User, request: FolderRequest):
    query = db.query(Note).filter(Note.user_id == user.id)

    if request.folder_id == -1:
        notes = query.all()
    elif request.folder_id == -2:
        notes = query.filter(Note.folder_id == None).all()
    else:
        notes = query.filter(Note.folder_id == request.folder_id).all()
    
    if not notes:
        raise HTTPException(status_code=404, detail="Notas no encontradas")
    return notes

def get_note_detail(db: Session, user: User, request: NoteRequest):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    note = db.query(Note).filter(Note.user_id == user.id, Note.id == request.note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Nota no encontradas")
    
    if note.ask_password:
        if not pwd_context.verify(request.master_password, user.password_hash):
            raise HTTPException(status_code=401, detail="Contraseña maestra incorrecta")

    try:
        decrypted_content = decrypt_content(note.content_encrypted)
    except InvalidToken:
        # Contraseña vieja sin cifrar
        decrypted_content = note.content_encrypted

    note_detail = NoteDetail(
        content=decrypted_content
    )

    return note_detail

async def delete_note(db: Session, user: User, request: NoteRequest):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    note = db.query(Note).filter(Note.user_id == user.id, Note.id == request.note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    
    if note.ask_password:
        if not pwd_context.verify(request.master_password, user.password_hash):
            raise HTTPException(status_code=401, detail="Contraseña maestra incorrecta")
        
    db.delete(note)
    db.commit()

    await manager.send_to_user(user.id, json.dumps({
        "type": "delete_note",
    }))

    return {"message": f"Nota eliminada correctamente"}

async def modify_note(db: Session, user: User, request: NoteRequest, new_data: NoteCreate):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    note = db.query(Note).filter(Note.user_id == user.id, Note.id == request.note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    
    existing = db.query(Note).filter(Note.user_id == user.id,Note.title == new_data.title, Note.id != request.note_id).first()
    if existing:
       raise HTTPException(status_code=409, detail="Titulo no disponible")
    
    if note.ask_password:
        if not pwd_context.verify(request.master_password, user.password_hash):
            raise HTTPException(status_code=401, detail="Contraseña maestra incorrecta")
        
    content_encrypted = fernet.encrypt(new_data.content.encode()).decode()
    
    note.title = new_data.title
    note.content_encrypted = content_encrypted
    note.ask_password = new_data.ask_master_password
    note.folder_id = new_data.folder_id

    db.add(note)
    db.commit()
    db.refresh(note)

    await manager.send_to_user(user.id, json.dumps({
        "type": "modify_note",
    }))

    return {"message": f"Nota modificada correctamente"}
    
