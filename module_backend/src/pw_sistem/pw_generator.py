import random
import string

from src.models.password_model import PasswordGenerate

def generate_password(options: PasswordGenerate):
    # Definir los grupos
    groups = []
    if options.include_lower:
        groups.append(string.ascii_lowercase)
    if options.include_number:
        groups.append(string.digits)
    if options.include_symbols:
        groups.append(string.punctuation)
    if options.include_capital:
        groups.append(string.ascii_uppercase)

    # Si la longitud solicitada es menor al mínimo requerido, error
    min_required = 2 * len(groups)
    if options.length < min_required:
        raise ValueError(f"La longitud mínima debe ser {min_required} para cumplir con la regla.")

    # Asegurar al menos 2 de cada grupo
    password_chars = []
    for group in groups:
        password_chars.extend(random.choices(group, k=2))

    # Rellenar el resto con cualquier caracter válido
    all_chars = "".join(groups)
    remaining = options.length - len(password_chars)
    password_chars.extend(random.choices(all_chars, k=remaining))

    # Barajar para evitar patrones
    random.shuffle(password_chars)

    return "".join(password_chars)