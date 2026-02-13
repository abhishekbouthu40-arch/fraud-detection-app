"""Load and run fraud detection model."""
import json
import pickle
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "fraud_model.pkl"
ENCODER_PATH = PROJECT_ROOT / "models" / "label_encoder.pkl"
MAPPING_PATH = PROJECT_ROOT / "models" / "type_mapping.json"

_model = None
_encoder = None
_type_mapping = None


def _load_artifacts():
    """Lazy load model and encoder."""
    global _model, _encoder, _type_mapping
    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Model not found at {MODEL_PATH}. Run 'python train.py' first."
            )
        with open(MODEL_PATH, "rb") as f:
            _model = pickle.load(f)
        with open(ENCODER_PATH, "rb") as f:
            _encoder = pickle.load(f)
        with open(MAPPING_PATH, "r") as f:
            _type_mapping = json.load(f)
    return _model, _encoder, _type_mapping


def predict(step: int, type_: str, amount: float, old_balance: float, new_balance: float) -> tuple[bool, float]:
    """
    Predict if transaction is fraud.
    Returns (is_fraud, confidence).
    """
    model, encoder, mapping = _load_artifacts()
    
    # Encode type (handle unknown types)
    type_upper = type_.upper().strip()
    if type_upper not in mapping:
        # Default to PAYMENT encoding if unknown
        type_upper = "PAYMENT"
    type_encoded = mapping.get(type_upper, 0)
    
    features = np.array([[step, type_encoded, amount, old_balance, new_balance]])
    pred = model.predict(features)[0]
    proba = model.predict_proba(features)[0]
    confidence = float(proba[int(pred)])
    
    return bool(pred), confidence
