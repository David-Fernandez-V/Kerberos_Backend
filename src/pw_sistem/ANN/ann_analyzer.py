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

def analyze_password(password):
    model, scaler = load_trained_model()

    features = extract_features(password)
    
    features = np.array(features).reshape(1, -1)
    features = scaler.transform(features)
    prediction = model.predict(features)
    strength_level = np.argmax(prediction)

    return strength_level
