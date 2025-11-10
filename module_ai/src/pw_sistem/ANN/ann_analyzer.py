import os
import pickle
import numpy as np
from tensorflow.keras.models import load_model

from src.pw_sistem.extract_features import extract_features

labels= ["Muy debil", "Debil", "Estandar", "Fuerte", "Muy fuerte"]

base_dir = os.path.dirname(os.path.abspath(__file__))
rockyou_path = os.path.join(base_dir, "rockyou.txt")

def load_trained_model():
    model = load_model("src/pw_sistem/ANN/classifier_model.h5")

    with open("src/pw_sistem/ANN/scaler.pkl", "rb") as f:
        scaler = pickle.load(f)

    return model, scaler

with open(rockyou_path, encoding="latin-1", errors="ignore") as f:
    common_words = set(line.strip().lower() for line in f if line.strip())

model, scaler = load_trained_model()

def analyze_password(password):
    features = extract_features(password)
    
    features = np.array(features).reshape(1, -1)
    features = scaler.transform(features)
    prediction = model.predict(features)
    strength_level = np.argmax(prediction)

    #revisión heurística

    pw_lower = password.lower()
    if pw_lower in common_words:
        strength_level = 0  # mínimo nivel

    elif len(password) <15:
        for word in common_words:
            if len(word) > 3 and word in pw_lower:  # umbral mínimo de 4 letras
                strength_level = max(0, strength_level - 1)  # penalizar un nivel
                break

    return strength_level

#lvl = analyze_password("contraseña")
#print("\n Nivel: "+lvl)
