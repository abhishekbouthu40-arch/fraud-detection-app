from fastapi.responses import JSONResponse

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

        prediction = model.predict([features])[0]

        return {
            "fraud": int(prediction)
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
