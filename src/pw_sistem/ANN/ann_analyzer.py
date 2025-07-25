import json
import pickle
import numpy as np
from tensorflow.keras.models import load_model

from src.pw_sistem.extract_features import extract_features

labels= ["Muy debil", "Debil", "Estandar", "Fuerte", "Muy fuerte"]

def load_trained_model():
    model = load_model("src/pw_sistem/ANN/classifier_model.h5")

    with open("src/pw_sistem/ANN/scaler.pkl", "rb") as f:
        scaler = pickle.load(f)

    return model, scaler

def is_common_password(password):
    with open("src/pw_sistem/rockyou.txt", encoding="latin-1")as f:
        for line in f:
            if password == line.strip():
                return True
        
        return False
    return 0

def analyze_password(password):
    message = ""
    model, scaler = load_trained_model()

    features = extract_features(password)
    
    features = np.array(features).reshape(1, -1)
    features = scaler.transform(features)
    prediction = model.predict(features)
    strength_level = np.argmax(prediction)

    if is_common_password(password):
        message = "Su contraseña se encuentra en una base de datos filtrada"

    #return {"message": f"Nivel de seguridad: {labels[strength_level]}. {message}"}
    return strength_level
