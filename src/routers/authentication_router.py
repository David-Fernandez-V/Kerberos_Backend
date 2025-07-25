from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.models.user_model import User, UserLogin
from src.services import auth_service
from src.services.auth_dependency import get_current_user

authentication_router = APIRouter()

#Ruta abierta
@authentication_router.post("/login", tags=["Authentication"])
def login(user: UserLogin, db: Session = Depends(get_db)):
    return auth_service.authenticate_user(db, user.email, user.password)

@authentication_router.post("/logout", tags=["Authentication"])
def logout():
    response = JSONResponse(content={"message": "Sesión cerrada"})
    response.delete_cookie("access_token")
    return response

@authentication_router.get("/me", tags=["Authentication"])
def get_me(current_user: User = Depends(get_current_user)):
    return {"email": current_user.email}

@authentication_router.get("/refresh", tags=["Authentication"])
def refresh_token(current_user: User = Depends(get_current_user)):
    return auth_service.refresh_token(current_user)

