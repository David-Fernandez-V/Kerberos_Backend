from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, Text, func
from sqlalchemy.orm import relationship
from src.models.folder_model import FolderOut
from src.database.db import Base

from pydantic import BaseModel

class Password(Base):
    __tablename__ = "passwords"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    service_name = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    password_encrypted = Column(Text, nullable=False)
    strength_level = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    web_page = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    ask_password = Column(Boolean, default=False)
    folder_id = Column(Integer, ForeignKey("folders.id",ondelete="SET NULL"),nullable=True)

    # Relaciones
    owner = relationship("User", back_populates="passwords")
    folder = relationship("Folder", back_populates="passwords")

class PasswordOut(BaseModel):
    id: int
    service_name: str
    strength_level: int #Considerar cambiarlo PasswordDetail
    web_page: Optional[str]
    ask_password: bool
    folder: Optional[FolderOut]

    class Config:
        orm_mode = True

class PasswordDetail(BaseModel):
    password: str
    username: str
    created_at: datetime
    updated_at: datetime
    notes: Optional[str]

class PasswordCreate(BaseModel):
    service_name: str
    username: str
    password: str
    ask_master_password: Optional[bool] = False
    web_page: Optional[str] = None
    notes: Optional[str] = None
    folder_id: Optional[int | None] = None

class PasswordGenerate(BaseModel):
    length: int
    include_capital: bool
    include_lower: bool
    include_number: bool
    include_symbols: bool

class PassphraseGenerate(BaseModel):
    words_number: int
    separator: str
    include_number: bool #revisar
    include_symbol: bool #revisar
    capitalize: bool
    english: bool
    spanish: bool

class PasswordRequest(BaseModel):
    password_id: int
    master_password: str = ""

class PasswordEdit(BaseModel):
    pass