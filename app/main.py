"""FastAPI application for fraud detection."""
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from app.schemas import TransactionInput, PredictionResponse
from app.model import predict as model_predict

app = FastAPI(
    title="Fraud Detection API",
    description="Online payment fraud detection using Random Forest",
    version="1.0.0",
)

# Mount static files
STATIC_DIR = Path(__file__).parent.parent / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the frontend."""
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return HTMLResponse("<h1>Fraud Detection API</h1><p>API is running. Add static/index.html for UI.</p>")


@app.get("/health")
async def health():
    """Health check for deployment."""
    return {"status": "healthy"}


@app.post("/api/predict", response_model=PredictionResponse)
async def predict_fraud(transaction: TransactionInput):
    """Predict if a transaction is fraudulent."""
    is_fraud, confidence = model_predict(
        step=transaction.step,
        type_=transaction.type,
        amount=transaction.amount,
        old_balance=transaction.old_balance,
        new_balance=transaction.new_balance,
    )
    return PredictionResponse(
        prediction="FRAUD" if is_fraud else "SAFE",
        confidence=round(confidence, 4),
        is_fraud=is_fraud,
    )
