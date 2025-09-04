import random
import csv
from pathlib import Path
from src.models.password_model import PassphraseGenerate

# Diccionario de rutas CSV
CSV_FILES = {
    "NOUN": "src/pw_sistem/dictionaries/nouns.csv",
    "VERB": "src/pw_sistem/dictionaries/verbs.csv",
    "ADJ": "src/pw_sistem/dictionaries/adjectives.csv",
    "ADV": "src/pw_sistem/dictionaries/adverbs.csv",
}

WORD_LISTS = {}

SYMBOLS = "!@#$%^&*"

def load_words(word_type: str):
    """Carga palabras desde CSV si no están en caché."""
    if word_type not in CSV_FILES:
        raise ValueError(f"No existe un CSV definido para {word_type}")

    if word_type not in WORD_LISTS:
        path = Path(CSV_FILES[word_type])
        if not path.exists():
            raise FileNotFoundError(f"Archivo {path} no encontrado")
        with open(path, encoding="utf-8") as f:
            reader = csv.reader(f)
            WORD_LISTS[word_type] = [row[0].strip() for row in reader if row]
    return WORD_LISTS[word_type]

def generate_structure(n: int):
    
    #base_pattern = ["ADJ", "NOUN", "VERB", "NOUN"]
    base_pattern = ["ADJ", "NOUN", "VERB", "ADV", "NOUN"]
    structure = [base_pattern[i % len(base_pattern)] for i in range(n)]
    return structure

def generate_passphrase(passphrase_config: PassphraseGenerate):
    # Crear estructura dinámica según words_number
    structure = generate_structure(passphrase_config.words_number)

    words = []
    for part in structure:
        try:
            word_list = load_words(part)
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