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

    #Elementos extra a insertar
    extras = []
    if passphrase_config.include_number:
        extras.append(str(random.randint(10, 99)))
    if passphrase_config.include_symbol:
        extras.append(random.choice(SYMBOLS))

    # Insertar inicio o final
    for extra in extras:
        if random.choice([True, False]):
            words.insert(0, extra)
        else:
            words.append(extra)

    # Separador
    passphrase = passphrase_config.separator.join(words)

    return passphrase