from typing import List, Optional
from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from src.models.folder_model import FolderRequest
from src.database.db import get_db
from src.models.password_model import PasswordCreate, PasswordOut, PasswordDetail, PasswordRequest, PasswordGenerate
from src.models.user_model import User
from src.services import password_service
from src.services.auth_dependency import get_current_user

password_router = APIRouter()

@password_router.post("/analyze", tags=["Passwords"])
def get_analasys(password: str = Body(..., embed=True)):
    return password_service.get_analyze_password(password)  

@password_router.post("/create", tags=["Passwords"])
def create_password(
    password_data: PasswordCreate ,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return password_service.create_password(db, password_data, current_user)

@password_router.post("/by-user", response_model=List[PasswordOut], tags=["Passwords"])
def get_passwords(
    request: FolderRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return password_service.get_passwords_by_user(db, current_user, request)

@password_router.post("/get_detail", response_model=PasswordDetail, tags=["Passwords"])
def get_password_detail(
    password_request: PasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return password_service.get_password_detail(db, current_user, password_request)

@password_router.delete("/delete", tags=["Passwords"])
def delete_password(
    password_request: PasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return password_service.delete_password(db, current_user, password_request)

@password_router.post("/generate", tags=["Passwords"])
def generate_password(
    pwd_options: PasswordGenerate,
    current_user: User = Depends(get_current_user),
):
    return password_service.generate_pwd(pwd_options)