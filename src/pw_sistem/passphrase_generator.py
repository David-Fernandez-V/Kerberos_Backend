import random

from src.models.password_model import PassphraseGenerate

NOUNS = ["tigre", "sol", "nube", "roca", "puerta", "luna", "fuego"]
VERBS = ["corre", "salta", "gira", "mira", "rompe", "conecta"]
ADJECTIVES = ["azul", "rápido", "silencioso", "invisible", "solido", "brillante"]

SYMBOLS = "!@#$%^&*"
NUMBERS = list(range(10))

def generate_passphrase(passphrase_config :PassphraseGenerate):
    structure=["ADJ", "NOUN", "VERB", "NOUN"]

    words = []

    for part in structure[:passphrase_config.words_number]:
        if part == "NOUN":
            word = random.choice(NOUNS)
        elif part == "VERB":
            word = random.choice(VERBS)
        elif part == "ADJ":
            word = random.choice(ADJECTIVES)
        else:
            word = "???"
        
        if passphrase_config.capitalize:
            word = word.capitalize()

        words.append(word)

    passphrase = passphrase_config.separator.join(words)

    if passphrase_config.include_number:
        number = str(random.randint(10, 99))
        passphrase += passphrase_config.separator + number

    if passphrase_config.include_symbol:
        symbol = random.choice(SYMBOLS)
        passphrase += symbol

    return passphrase