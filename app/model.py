import os
import pickle
import json
import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

MODEL_PATH = os.path.join(BASE_DIR, "models", "fraud_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "models", "label_encoder.pkl")
MAPPING_PATH = os.path.join(BASE_DIR, "models", "type_mapping.json")

_model = None
_encoder = None
_type_mapping = None


def _load_artifacts():
    global _model, _encoder, _type_mapping

    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

        with open(MODEL_PATH, "rb") as f:
            _model = pickle.load(f)

        with open(ENCODER_PATH, "rb") as f:
            _encoder = pickle.load(f)

        with open(MAPPING_PATH, "r") as f:
            _type_mapping = json.load(f)

    return _model, _encoder, _type_mapping


def predict(step, type_, amount, old_balance, new_balance):
    model, encoder, mapping = _load_artifacts()

    type_upper = type_.upper().strip()
    type_encoded = mapping.get(type_upper, mapping.get("PAYMENT", 0))

    features = np.array([[step, type_encoded, amount, old_balance, new_balance]])

    pred = model.predict(features)[0]
    proba = model.predict_proba(features)[0]

    confidence = float(proba[int(pred)])

    return bool(pred), confidence
