"""
Generate sample fraud detection transaction dataset.
Run: python data/generate_dataset.py
"""
import csv
import random
from pathlib import Path

TRANSACTION_TYPES = ["PAYMENT", "TRANSFER", "CASH_OUT", "CASH_IN", "DEBIT"]
FRAUD_TYPES = ["TRANSFER", "CASH_OUT"]  # Fraud often involves these
SAFE_TYPES = ["PAYMENT", "CASH_IN", "DEBIT"]

def generate_dataset(n_samples: int = 5000, fraud_ratio: float = 0.05) -> None:
    """Generate synthetic transaction data for fraud detection."""
    data = []
    n_fraud = int(n_samples * fraud_ratio)
    n_safe = n_samples - n_fraud
    
    random.seed(42)
    
    # Generate fraud transactions
    for _ in range(n_fraud):
        step = random.randint(1, 744)  # Time steps (hours in ~31 days)
        txn_type = random.choice(FRAUD_TYPES)
        amount = random.uniform(100, 50000)
        old_balance = random.uniform(1000, 100000)
        new_balance = old_balance - amount
        if new_balance < 0:
            new_balance = 0
        data.append({
            "step": step, "type": txn_type, "amount": round(amount, 2),
            "oldbalanceOrg": round(old_balance, 2), "newbalanceOrig": round(new_balance, 2),
            "oldbalanceDest": round(random.uniform(0, 50000), 2),
            "newbalanceDest": round(random.uniform(0, 100000), 2),
            "isFraud": 1
        })
    
    # Generate safe transactions
    for _ in range(n_safe):
        step = random.randint(1, 744)
        txn_type = random.choice(TRANSACTION_TYPES)
        amount = random.uniform(1, 10000)
        old_balance = random.uniform(500, 50000)
        new_balance = old_balance - amount if txn_type in ["PAYMENT", "TRANSFER", "CASH_OUT", "DEBIT"] else old_balance + amount
        if new_balance < 0:
            new_balance = 0
        data.append({
            "step": step, "type": txn_type, "amount": round(amount, 2),
            "oldbalanceOrg": round(old_balance, 2), "newbalanceOrig": round(new_balance, 2),
            "oldbalanceDest": round(random.uniform(0, 50000), 2),
            "newbalanceDest": round(random.uniform(0, 100000), 2),
            "isFraud": 0
        })
    
    random.shuffle(data)
    
    output_path = Path(__file__).parent / "sample_transactions.csv"
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Generated {len(data)} transactions ({n_fraud} fraud, {n_safe} safe) -> {output_path}")

if __name__ == "__main__":
    generate_dataset()
