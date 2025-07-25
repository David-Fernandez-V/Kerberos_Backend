from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from src.database.db import Base

from pydantic import BaseModel, EmailStr, Field

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    deleted = Column(Boolean, nullable=False, default=False)

    # Relaciones
    folders = relationship("Folder", back_populates="user", cascade="all, delete-orphan", passive_deletes=True)
    passwords = relationship("Password", back_populates="owner")
    notes = relationship("Note", back_populates="owner")
    cards = relationship("Card", back_populates="owner")

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field (...,min_length=5)

class UserLogin(BaseModel):
    email: EmailStr
    password: str
