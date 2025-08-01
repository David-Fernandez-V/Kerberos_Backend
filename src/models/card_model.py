from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, SmallInteger,String, Text, Boolean, ForeignKey, DateTime, Text, func
from sqlalchemy.orm import relationship
from src.models.folder_model import FolderOut
from src.database.db import Base

from pydantic import BaseModel

class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)

    alias = Column(String(255), nullable=False)
    cardholder_name = Column(String(255), nullable=False)
    number_encrypted = Column(Text, nullable=False)
    last4 = Column(String(4), nullable=False)
    expiration_month = Column(Text, nullable=False)
    expiration_year = Column(Text, nullable=False)

    #opcionales
    csv_encrypted = Column(Text, nullable=True)
    brand = Column(String(255), nullable=True)
    type = Column(String(10), nullable=True)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    ask_password = Column(Boolean, default=False)
    folder_id = Column(Integer, ForeignKey("folders.id",ondelete="SET NULL"),nullable=True)

    # Relaciones
    owner = relationship("User", back_populates="cards")
    folder = relationship("Folder", back_populates="cards")

class CardOut(BaseModel):
    id: int
    alias: str
    last4: str
    brand: Optional[str]
    type: Optional[str]
    ask_password: bool
    folder: Optional[FolderOut]

    class Config:
        orm_mode = True

class CardDetail(BaseModel):
    cardholder_name: str
    number: str
    expiration_month: str
    expiration_year: str
    csv: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class CardCreate(BaseModel):
    alias: str
    cardholder_name: str
    number: str
    expiration_month: str
    expiration_year: str
    type: Optional[str] = None
    csv: Optional[str] = None
    brand: Optional[str] = None
    notes: Optional[str] = None
    folder_id: Optional[int | None] = None
    ask_master_password: Optional[bool] = False

class CardRequest(BaseModel):
    card_id: int
    master_password: str = ""

class CardEdit(BaseModel):
    pass