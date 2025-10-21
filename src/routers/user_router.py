from fastapi import APIRouter, Path, Depends
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.models.user_model import ChangeEmailRequest, ChangeNameRequest, ChangePasswordRequest, User, UserCreate, UserRequest
from src.services import user_service
from src.services.auth_dependency import get_current_user

user_router = APIRouter()

#Registrar usuario (Libre)
@user_router.post("/register", tags=["Users"])
def create_user(
        user_data: UserCreate, db: Session = Depends(get_db),        
    ):
    return user_service.create_user(db, user_data)

@user_router.post("/change-password", tags=["Users"])
async def change_password(
    request: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await user_service.change_password(db, current_user, request)

@user_router.post("/change-name", tags=["Users"])
async def change_name(
    request: ChangeNameRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await user_service.change_name(db, current_user, request)

@user_router.post("/change-email", tags=["Users"])
async def change_name(
    token: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await user_service.change_email(db, current_user, token)

@user_router.post("/request-email-change", tags=["Users"])
def request_email_change(
    request: ChangeEmailRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return user_service.request_email_change(db, current_user, request)

@user_router.get("/me", tags=["Users"])
def get_me(
    current_user: User = Depends(get_current_user)
):
    return user_service.get_profile(current_user)

@user_router.post("/check-masterpassword",tags=["Users"])
def check_password(
    request: UserRequest,
    
    current_user: User = Depends(get_current_user),
):
    return user_service.check_master_password(current_user, request)

    