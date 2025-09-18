from fastapi import APIRouter, Path, Depends
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.models.user_model import User, UserCreate, UserRequest
from src.services import user_service
from src.services.auth_dependency import get_current_user

user_router = APIRouter()

#Registrar usuario (Libre)
@user_router.post("/register", tags=["Users"])
def create_user(
        user_data: UserCreate, db: Session = Depends(get_db),        
    ):
    return user_service.create_user(db, user_data)

@user_router.put("/change-password/{user_id}", tags=["Users"])
def change_password(
        user_id: int, new_password: str, db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)    
    ):
    return user_service.change_password(db, user_id, new_password)

@user_router.put("/me", tags=["Users"])
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user

@user_router.put("/delete-user/{user_id}", tags=["Users"])
def delete_user(
        user_id: int, db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
    return user_service.delete_user(db, user_id)

@user_router.delete("/destroy-user/{user_id}", tags=["Users"])
def destroy_user(
        user_id: int, db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
    return user_service.destroy_user(db, user_id)

@user_router.post("/check-masterpassword",tags=["Users"])
def check_password(
    request: UserRequest,
    
    current_user: User = Depends(get_current_user),
):
    return user_service.check_master_password(current_user, request)

    