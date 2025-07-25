from sqlalchemy.orm import Session
from src.models.user_model import User, UserCreate
from passlib.context import CryptContext
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"])

def get_users(db: Session):
    users = db.query(User).filter(User.deleted == False).all()
    if not users:
        raise HTTPException(status_code=404, detail="Sin usuarios registrados")
    return users

def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.deleted == False, User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

def get_user_by_email(db: Session, email: str):
    user = db.query(User).filter(User.deleted == False, User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

def create_user(db: Session, user_data: UserCreate):
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Correo ya registrado")
    hashed_password = pwd_context.hash(user_data.password)
    new_user = User(email=user_data.email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": f"Usuario registrado con exito: {new_user.email}"}

def change_password(db: Session, user_id: int, new_password: str):
    user = db.query(User).filter(User.deleted == False, User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    hashed_password = pwd_context.hash(new_password)
    user.password_hash = hashed_password
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": f"Contraseña actualizada para el correo: {user.email}"}

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.deleted == False, User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user.deleted = True
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message:": f"Usuario eliminado correctamente: {user.email}"}

def destroy_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(user)
    db.commit()
    return {"message:": f"Usuario eliminado correctamente: {user.email}"}
