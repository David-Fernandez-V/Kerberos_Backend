import random
import csv
from pathlib import Path
from src.pw_sistem.password_model import PassphraseGenerate

# Diccionario de rutas CSV
BASE_CSV_FILES = {
    "NOUN": "nouns.csv",
    "VERB": "verbs.csv",
    "ADJ": "adjectives.csv",
    "ADV": "adverbs.csv",
}

WORD_LISTS = {}
SYMBOLS = "!@#$%^&*"

def load_words(word_type: str, spanish: bool = False):
    """Carga palabras desde CSV si no están en caché, según el idioma."""
    lang_folder = "es" if spanish else "en"
    
    # Construir ruta completa usando tu estructura base
    base_path = Path(__file__).parent.parent / "pw_sistem" / "dictionaries" / lang_folder
    path = base_path / BASE_CSV_FILES[word_type]

    # Cache key única para idioma + tipo
    cache_key = f"{lang_folder}/{word_type}"

    if cache_key not in WORD_LISTS:
        if not path.exists():
            raise FileNotFoundError(f"Archivo {path} no encontrado")
        with open(path, encoding="utf-8") as f:
            reader = csv.reader(f)
            WORD_LISTS[cache_key] = [row[0].strip() for row in reader if row]

    return WORD_LISTS[cache_key]

def generate_structure(n: int):
    base_pattern = ["ADJ", "NOUN", "VERB", "ADV", "NOUN"]
    structure = [base_pattern[i % len(base_pattern)] for i in range(n)]
    return structure

def generate_passphrase(passphrase_config: PassphraseGenerate):
    # Crear estructura dinámica según words_number
    structure = generate_structure(passphrase_config.words_number)

    words = []
    for part in structure:
        try:
            word_list = load_words(part, spanish=passphrase_config.spanish)
            word = random.choice(word_list)
        except Exception:
            word = "???"

        if passphrase_config.capitalize:
            word = word.capitalize()
        words.append(word)

    # Extras: número y símbolo
    extras = []
    if passphrase_config.include_number:
        extras.append(str(random.randint(10, 99)))
    if passphrase_config.include_symbol:
        extras.append(random.choice(SYMBOLS))

    # Insertar extras al inicio o final
    for extra in extras:
        if random.choice([True, False]):
            words.insert(0, extra)
        else:
            words.append(extra)

    # Unir con separador
    passphrase = passphrase_config.separator.join(words)
    return passphrase