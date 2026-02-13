import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

MODEL_PATH = os.path.join(ROOT_DIR, "models", "fraud_model.pkl")
ENCODER_PATH = os.path.join(ROOT_DIR, "models", "label_encoder.pkl")
