"""
Train Random Forest fraud detection model.
Run: python train.py
"""
import json
import pickle
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder

# Paths
PROJECT_ROOT = Path(__file__).parent
DATA_PATH = PROJECT_ROOT / "data" / "sample_transactions.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "fraud_model.pkl"
ENCODER_PATH = PROJECT_ROOT / "models" / "label_encoder.pkl"


def load_and_prepare_data():
    """Load dataset and prepare features."""
    df = pd.read_csv(DATA_PATH)
    
    # Encode transaction type
    le = LabelEncoder()
    df["type_encoded"] = le.fit_transform(df["type"].astype(str))
    
    # Features for prediction (matching API input)
    feature_cols = ["step", "type_encoded", "amount", "oldbalanceOrg", "newbalanceOrig"]
    X = df[feature_cols]
    y = df["isFraud"]
    
    return X, y, le


def train():
    """Train Random Forest model and save."""
    print("Loading data...")
    X, y, le = load_and_prepare_data()
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print("Training Random Forest...")
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Safe", "Fraud"]))
    
    # Save model and encoder
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    with open(ENCODER_PATH, "wb") as f:
        pickle.dump(le, f)
    
    # Save type mapping for API (convert numpy int64 to Python int for JSON)
    type_mapping = {str(k): int(v) for k, v in zip(le.classes_, le.transform(le.classes_))}
    mapping_path = PROJECT_ROOT / "models" / "type_mapping.json"
    with open(mapping_path, "w") as f:
        json.dump(type_mapping, f, indent=2)
    
    print(f"\nModel saved to {MODEL_PATH}")
    print(f"Encoder saved to {ENCODER_PATH}")


if __name__ == "__main__":
    train()
