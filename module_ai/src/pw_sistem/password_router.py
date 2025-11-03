from fastapi import APIRouter, Body
from src.pw_sistem.password_model import PasswordGenerate, PassphraseGenerate
from src.pw_sistem import password_service

password_router = APIRouter()

@password_router.post("/analyze", tags=["Passwords"])
def get_analasys(password: str = Body(..., embed=True)):
    return password_service.get_analyze_password(password)  

@password_router.post("/generate_passwords", tags=["Passwords"])
def generate_password(
    pwd_options: PasswordGenerate,
):
    return password_service.generate_psw(pwd_options)

@password_router.post("/generate_passphrase", tags=["Passwords"])
def generate_passphrase(
    pwd_options: PassphraseGenerate,
):
    return password_service.generate_psphrase(pwd_options)