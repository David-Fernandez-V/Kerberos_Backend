import math
from collections import Counter

def compute_entropy(pw):
    if not pw:
        return 0
    counts = Counter(pw)
    length = len(pw)
    entropy = -sum((count / length) * math.log2(count / length) for count in counts.values())
    return entropy

def extract_features(pw):
    length = len(pw)
    num_digits = sum(c.isdigit() for c in pw)
    num_lowercase = sum(c.islower() for c in pw)
    num_uppercase = sum(c.isupper() for c in pw)
    num_special_chars = sum(not c.isalnum() for c in pw)
    
    char_count = {}
    max_consecutive_chars = 1
    current_streak = 1
    char_type_changes = 0
    prev_type = None

    for i, c in enumerate(pw):
        # Caracter repetido
        char_count[c] = char_count.get(c, 0) + 1

        # Consecutivos
        if i > 0 and pw[i] == pw[i-1]:
            current_streak += 1
            max_consecutive_chars = max(max_consecutive_chars, current_streak)
        else:
            current_streak = 1

        # Tipo de carácter
        if c.isdigit():
            t = 'digit'
        elif c.islower():
            t = 'lower'
        elif c.isupper():
            t = 'upper'
        else:
            t = 'special'

        if prev_type and t != prev_type:
            char_type_changes += 1
        prev_type = t

    char_repea = sum(count - 1 for count in char_count.values() if count > 1)
    entropy = compute_entropy(pw)

    return [
        length, num_digits, num_lowercase, num_uppercase, num_special_chars,
        char_repea, max_consecutive_chars, char_type_changes, entropy
    ]