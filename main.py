from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from tensorflow.keras.models import load_model
from utils import preprocess_input, scaler, window_size
from fastapi.middleware.cors import CORSMiddleware


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou especifique ["http://127.0.0.1:5500"] se quiser mais seguro
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI(
    title="API de Previsão de Preço com LSTM",
    description="Esta API recebe os 60 últimos preços normalizados e retorna a previsão do próximo valor com uma rede neural LSTM treinada.",
    version="1.0.0"
)
model = load_model("modelo_lstm_dis.h5")

class PriceRequest(BaseModel):
    prices: list[float]  # lista com os últimos 60 preços normalizados

@app.get("/")
def read_root():
    return {"message": "API LSTM funcionando. Use POST /predict para previsões."}

@app.post("/predict")
def predict_price(data: PriceRequest):
    if len(data.prices) != window_size:
        raise HTTPException(status_code=400, detail=f"É necessário enviar exatamente {window_size} preços.")

    try:
        X_input = preprocess_input(data.prices)  # formata entrada para (1, 60, 1)
        pred_scaled = model.predict(X_input)
        pred_real = scaler.inverse_transform(pred_scaled)
        return {"previsao": float(round(pred_real[0][0], 2))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
