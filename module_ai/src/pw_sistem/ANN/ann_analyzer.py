import os
import pickle
import numpy as np
from tensorflow.keras.models import load_model

from src.pw_sistem.extract_features import extract_features

labels = ["Muy débil", "Débil", "Estándar", "Fuerte", "Muy fuerte"]

# Ruta
base_dir = os.path.dirname(os.path.abspath(__file__))
rockyou_path = os.path.join(base_dir, "rockyou.txt")

# Cargar modelo
def load_trained_model():
    model = load_model(os.path.join(base_dir, "classifier_model.h5"))
    with open(os.path.join(base_dir, "scaler.pkl"), "rb") as f:
        scaler = pickle.load(f)
    return model, scaler


model, scaler = load_trained_model()


#buscar la contraseña en rockyou
def is_common_password(password, filepath=rockyou_path):
    pw_lower = password.lower()
    try:
        with open(filepath, encoding="latin-1", errors="ignore") as f:
            for line in f:
                if line.strip().lower() == pw_lower:
                    return True
    except Exception as e:
        print(f"[Warning] Error leyendo rockyou.txt: {e}")
    return False


#Análisis 
def analyze_password(password):
    #Extraer características
    features = extract_features(password)
    features = np.array(features).reshape(1, -1)
    features = scaler.transform(features)

    #Predicción con la red neuronal
    prediction = model.predict(features, verbose=0)
    strength_level = np.argmax(prediction)

    #Revisión heurística (rockyou y substrings)
    pw_lower = password.lower()

    # Caso 1: Contraseña aparece exactamente en rockyou.txt
    if is_common_password(pw_lower):
        strength_level = 0  # mínimo nivel

    # Caso 2: Subcadenas comunes
    elif len(password) < 15:
        try:
            with open(rockyou_path, encoding="latin-1", errors="ignore") as f:
                for line in f:
                    word = line.strip().lower()
                    if len(word) > 3 and word in pw_lower:
                        strength_level = max(0, strength_level - 1)
                        break
        except Exception as e:
            print(f"[Warning] Error leyendo rockyou.txt: {e}")

    return strength_level
