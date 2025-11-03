from fastapi import HTTPException
from src.pw_sistem.password_model import PasswordGenerate, PassphraseGenerate
from src.pw_sistem.pw_generator import generate_password
from src.pw_sistem.passphrase_generator import generate_passphrase
from src.pw_sistem.ANN.ann_analyzer import analyze_password
from src.pw_sistem.pw_generator import generate_password
from src.pw_sistem.passphrase_generator import generate_passphrase

def get_analyze_password(password: str):
    try:
        return {"strength_level": int(analyze_password(password))}
    except Exception:
        raise HTTPException(status_code=500, detail="Error al analizar la contraseña")
    
def generate_psw(pwd_options: PasswordGenerate):
    try:
        return {"password": generate_password(pwd_options)}
    except Exception:
        raise HTTPException(status_code=500, detail="Error al generar contraseña")
    
def generate_psphrase(pwd_options: PassphraseGenerate):
    try:
        return {"passphrase": generate_passphrase(pwd_options)}
    except Exception:
        raise HTTPException(status_code=500, detail="Error al generar contraseña")