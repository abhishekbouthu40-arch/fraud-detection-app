from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.schemas import InputData
from app.model import predict_fraud

app = FastAPI()

@app.post("/predict")
def predict(data: InputData):
    try:
        features = [
            data.amount,
            data.transaction_type,
            data.old_balance,
            data.new_balance,
            data.time_step
        ]

        result = predict_fraud(features)

        return {"fraud": int(result)}

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
