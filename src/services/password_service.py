import os
from sqlalchemy.orm import Session
from fastapi import HTTPException
from cryptography.fernet import Fernet, InvalidToken
from dotenv import load_dotenv
from passlib.context import CryptContext

from src.models.folder_model import FolderRequest
from src.models.password_model import Password, PasswordCreate, PasswordRequest, PasswordDetail, PasswordGenerate, PassphraseGenerate
from src.models.user_model import User
from src.pw_sistem.pw_generator import generate_password
from src.pw_sistem.passphrase_generator import generate_passphrase
from src.pw_sistem.ANN.ann_analyzer import analyze_password
from src.pw_sistem.pw_generator import generate_password
from src.pw_sistem.passphrase_generator import generate_passphrase

load_dotenv()
fernet = Fernet(os.getenv("ENCRYPTION_KEY").encode())

def decrypt_password(encrypted_password: str) -> str:
    return fernet.decrypt(encrypted_password.encode()).decode()

def create_password(db: Session, password_data: PasswordCreate, user: User):
    existing = db.query(Password).filter(Password.user_id == user.id,Password.service_name == password_data.service_name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Nombre no disponible")
    
    strength = int(analyze_password(password_data.password))
    encrypted_password = fernet.encrypt(password_data.password.encode()).decode()

    new_password = Password(
        user_id = user.id,
        service_name = password_data.service_name,
        username = password_data.username,
        password_encrypted = encrypted_password,
        web_page = str(password_data.web_page),
        notes = password_data.notes,
        ask_password = password_data.ask_master_password,
        strength_level = strength,
        folder_id = password_data.folder_id
    )
    db.add(new_password)
    db.commit()
    db.refresh(new_password)
    return {"message": f"Contraseña guardada: {new_password.service_name}"}

def get_analyze_password(password: str):
    try:
        return {"strength_level": int(analyze_password(password))}
    except Exception:
        raise HTTPException(status_code=500, detail="Error al analizar la contraseña")
    
def get_passwords_by_user(db: Session, user: User, request: FolderRequest):
    query = db.query(Password).filter(Password.user_id == user.id)

    if request.folder_id == -1:
        passwords = query.all()
    elif request.folder_id == -2:
        passwords = query.filter(Password.folder_id == None).all()
    else:
        passwords = query.filter(Password.folder_id == request.folder_id).all()
    
    if not passwords:
        raise HTTPException(status_code=404, detail="Contraseñas no encontradas")

    return passwords

def get_password_detail(db: Session, user: User, request: PasswordRequest):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    password = db.query(Password).filter(Password.user_id == user.id, Password.id == request.password_id).first()

    if not password:
        raise HTTPException(status_code=404, detail="Contraseña no encontradas")
    
    if password.ask_password:
        if not pwd_context.verify(request.master_password, user.password_hash):
            raise HTTPException(status_code=401, detail="Contraseña maestra incorrecta")

    try:
        decrypted_password = decrypt_password(password.password_encrypted)
    except InvalidToken:
        # Contraseña vieja sin cifrar
        decrypted_password = password.password_encrypted

    password_detail = PasswordDetail(
        password = decrypted_password,
        username = password.username,
        created_at = password.created_at,
        updated_at = password.updated_at,
        notes = password.notes, 
    )

    return password_detail

def delete_password(db: Session, user: User, request: PasswordRequest):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    password = db.query(Password).filter(Password.user_id == user.id, Password.id == request.password_id).first()
    if not password:
        raise HTTPException(status_code=404, detail="Contraseña no encontrada")
    
    if password.ask_password:
        if not pwd_context.verify(request.master_password, user.password_hash):
            raise HTTPException(status_code=401, detail="Contraseña maestra incorrecta")
        
    db.delete(password)
    db.commit()
    return {"message:": f"Sesión eliminado correctamente"}

def generate_psw(pwd_options: PasswordGenerate):
    try:
        return {"password": generate_password(pwd_options)}
    except Exception:
        raise HTTPException(status_code=500, detail="Error al generar contraseña")
    
def generate_psphrase(pwd_options: PassphraseGenerate):
    try:
        return {"passphrase": generate_passphrase(pwd_options)}
    except Exception:
        raise HTTPException(status_code=500, detail="Error al generar contraseña")