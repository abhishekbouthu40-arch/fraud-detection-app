# Fraud Shield – Online Payment Fraud Detection

A production-ready web application that detects fraudulent payment transactions using a Random Forest machine learning model.

## Project Structure

```
fraud_detection_app/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── model.py         # ML model loading & prediction
│   └── schemas.py       # Pydantic request/response schemas
├── data/
│   ├── generate_dataset.py      # Dataset generator
│   └── sample_transactions.csv  # Sample transaction data
├── models/
│   ├── fraud_model.pkl      # Trained Random Forest (generated)
│   ├── label_encoder.pkl    # Transaction type encoder (generated)
│   └── type_mapping.json    # Type-to-id mapping (generated)
├── static/
│   ├── index.html        # Frontend UI
│   ├── style.css         # Styles
│   └── app.js            # Client-side logic
├── train.py              # Model training script
├── requirements.txt
├── render.yaml           # Render deployment
├── Procfile              # Railway / Heroku
├── nixpacks.toml         # Nixpacks build config
├── railway.json          # Railway config
└── README.md
```

## Run Instructions

### 1. Create virtual environment (recommended)

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Generate dataset (if needed)

```bash
python data/generate_dataset.py
```

### 4. Train the model

```bash
python train.py
```

### 5. Start the server

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

Open **http://localhost:8000** in your browser.

## API

### `POST /api/predict`

Request body:

```json
{
  "amount": 1500.0,
  "type": "TRANSFER",
  "old_balance": 5000.0,
  "new_balance": 3500.0,
  "step": 120
}
```

Response:

```json
{
  "prediction": "SAFE",
  "confidence": 0.9823,
  "is_fraud": false
}
```

### `GET /health`

Health check endpoint for deployment platforms.

## Deployment

### Render

1. Push this repo to GitHub.
2. Create a new Web Service on [Render](https://render.com).
3. Connect the repo.
4. Render will use `render.yaml` for configuration.
5. Build command (included in blueprint): dataset generation + training.
6. Start command: `gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`

### Railway

1. Push this repo to GitHub.
2. Create a new project on [Railway](https://railway.app).
3. Connect the repo and deploy.
4. Railway uses `nixpacks.toml` and `railway.json` for build and start.

### Manual production run

```bash
gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Features

- **Random Forest model** for fraud classification
- **5 input features**: Amount, Transaction type, Old balance, New balance, Time step
- **FastAPI backend** with validation and docs
- **Responsive web UI** with clear SAFE/FRAUD output and confidence
- **Health check** for orchestration and load balancers
- **Deployment configs** for Render and Railway

## License

MIT
