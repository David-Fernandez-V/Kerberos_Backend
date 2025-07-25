from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from src.database.db import Base  

# --- Modelo Folder ---
class Folder(Base):
    __tablename__ = "folders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relaciones
    user = relationship("User", back_populates="folders")
    passwords = relationship("Password", back_populates="folder", cascade="all, delete-orphan", passive_deletes=True)
    notes = relationship("Note", back_populates="folder", cascade="all, delete-orphan", passive_deletes=True)
    cards = relationship("Card", back_populates="folder", cascade="all, delete-orphan", passive_deletes=True)

class FolderOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class FolderCreate(BaseModel):
    name: str

class FolderModify(BaseModel):
    name: str

class FolderRequest(BaseModel):
    folder_id: int

