import os
from sqlalchemy.orm import Session
from fastapi import HTTPException
from cryptography.fernet import Fernet, InvalidToken
from dotenv import load_dotenv
from passlib.context import CryptContext

from src.models.folder_model import FolderRequest
from src.models.card_model import Card, CardCreate, CardRequest, CardDetail
from src.models.user_model import User

load_dotenv()
fernet = Fernet(os.getenv("ENCRYPTION_KEY").encode())

def decrypt(encrypted_content: str) -> str:
    return fernet.decrypt(encrypted_content.encode()).decode()

def create_card(db: Session, card_data: CardCreate, user: User):
    existing = db.query(Card).filter(Card.user_id == user.id, Card.alias == card_data.alias).first()
    if existing:
        raise HTTPException(status_code=409, detail="Nombre no disponible")
    
    number_encrypted = fernet.encrypt(card_data.number.encode()).decode()
    cardholder_name_encrypted = fernet.encrypt(card_data.cardholder_name.encode()).decode()
    expiration_month_encrypted = fernet.encrypt(str(card_data.expiration_month).encode()).decode()
    expiration_year_encrypted = fernet.encrypt(str(card_data.expiration_year).encode()).decode()
    
    if(card_data.csv):
        csv_encrypetd = fernet.encrypt(card_data.csv.encode()).decode()
    else:
        csv_encrypetd = None

    new_card = Card(
        user_id = user.id,
        alias = card_data.alias,
        cardholder_name = cardholder_name_encrypted,
        number_encrypted = number_encrypted,
        last4 = card_data.number[-4:], #Evaluar si es necesario
        expiration_month = expiration_month_encrypted,
        expiration_year = expiration_year_encrypted,
        csv_encrypted = csv_encrypetd,
        brand = card_data.brand,
        type = card_data.type,
        notes = card_data.notes,
        ask_password = card_data.ask_master_password,
        folder_id = card_data.folder_id
    )
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return {"message": f"Tarjeta guardada: {new_card.alias}"}

def get_cards_by_user(db: Session, user: User, request: FolderRequest):
    query = db.query(Card).filter(Card.user_id == user.id)

    if request.folder_id == -1:
        cards = query.all()
    elif request.folder_id == -2:
        cards = query.filter(Card.folder_id == None).all()
    else:
        cards = query.filter(Card.folder_id == request.folder_id).all()
    
    if not cards:
        raise HTTPException(status_code=404, detail="Tarjetas no encontradas")

    return cards

def get_card_detail(db: Session, user: User, request: CardRequest):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    card = db.query(Card).filter(Card.user_id == user.id, Card.id == request.card_id).first()

    if not card:
        raise HTTPException(status_code=404, detail="Tarjetas no encontradas")
    
    if card.ask_password:
        if not pwd_context.verify(request.master_password, user.password_hash):
            raise HTTPException(status_code=401, detail="Contraseña maestra incorrecta")

    #Desenpritación
    try:
        decrypted_number = decrypt(card.number_encrypted)
    except InvalidToken:
        decrypted_number = card.number_encrypted

    try:
        decrypted_cardholder_name = decrypt(card.cardholder_name)
    except InvalidToken:
        decrypted_cardholder_name = card.cardholder_name

    try:
        decrypted_expiration_month = decrypt(card.expiration_month)
    except InvalidToken:
        decrypted_expiration_month = card.expiration_month

    try:
        decrypted_expiration_year = decrypt(card.expiration_year)
    except InvalidToken:
        # Contraseña vieja sin cifrar
        decrypted_expiration_year = card.expiration_year

    if card.csv_encrypted:
        try:
            decrypted_csv = decrypt(card.csv_encrypted)
        except:
            decrypted_csv = card.csv_encrypted
    else:
        decrypted_csv = card.csv_encrypted

    card_detail = CardDetail(
        cardholder_name = decrypted_cardholder_name,
        number= decrypted_number,
        expiration_month = decrypted_expiration_month,
        expiration_year = decrypted_expiration_year,
        csv = decrypted_csv,
        notes = card.notes,
        created_at = card.created_at,
        updated_at = card.updated_at, 
    )

    return card_detail

def delete_card(db: Session, user: User, request: CardRequest):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    card = db.query(Card).filter(Card.user_id == user.id, Card.id == request.card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    
    if card.ask_password:
        if not pwd_context.verify(request.master_password, user.password_hash):
            raise HTTPException(status_code=401, detail="Contraseña maestra incorrecta")
        
    db.delete(card)
    db.commit()
    return {"message:": f"Tarjeta eliminada correctamente"}