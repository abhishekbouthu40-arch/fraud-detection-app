import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "fraud_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "..", "models", "label_encoder.pkl")
