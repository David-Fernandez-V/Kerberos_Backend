import random
import string

from src.models.password_model import PasswordGenerate

def generate_password(options: PasswordGenerate):
    # Combine digits, letters, and punctuation as possible characters for the password
    characters = string.digits + string.ascii_letters + string.punctuation
    # Randomly select characters and join them to form the password
    generated_password = "".join(random.choice(characters) for _ in range(options.length))
    return generated_password