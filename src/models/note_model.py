from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, Text, func
from sqlalchemy.orm import relationship
from src.models.folder_model import FolderOut
from src.database.db import Base

from pydantic import BaseModel

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    title = Column(String(255), nullable=False)
    content_encrypted = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    ask_password = Column(Boolean, default=False)
    folder_id = Column(Integer, ForeignKey("folders.id",ondelete="SET NULL"),nullable=True)

    # Relaciones
    owner = relationship("User", back_populates="notes")
    folder = relationship("Folder", back_populates="notes")

class NoteOut(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    ask_password: bool
    folder: Optional[FolderOut]

    class Config:
        orm_mode = True

class NoteDetail(BaseModel):
    content: str

class NoteRequest(BaseModel):
    note_id: int
    master_password: str = ""

class NoteCreate(BaseModel):
    title: str
    content: str
    ask_master_password: Optional[bool] = False
    folder_id: Optional[int | None] = None

class NoteEdit(BaseModel):
    pass