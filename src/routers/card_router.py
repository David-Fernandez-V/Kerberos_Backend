from typing import List, Optional
from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from src.models.folder_model import FolderRequest
from src.database.db import get_db
from src.models.card_model import CardCreate, CardOut, CardDetail, CardRequest
from src.models.user_model import User
from src.services import card_service
from src.services.auth_dependency import get_current_user

card_router = APIRouter()

@card_router.post("/create", tags=["Cards"])
def create_card(
    card_data: CardCreate ,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return card_service.create_card(db, card_data, current_user)

@card_router.post("/by-user", response_model=List[CardOut], tags=["Cards"])
def get_cards(
    request: FolderRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return card_service.get_cards_by_user(db, current_user, request)

@card_router.post("/get_detail", response_model=CardDetail, tags=["Cards"])
def get_card_detail(
    card_request: CardRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return card_service.get_card_detail(db, current_user, card_request)

@card_router.delete("/delete", tags=["Cards"])
def delete_card(
    card_request: CardRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return card_service.delete_card(db, current_user, card_request)