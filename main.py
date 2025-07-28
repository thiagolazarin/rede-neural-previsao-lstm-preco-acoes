from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from tensorflow.keras.models import load_model
from utils import preprocess_input, scaler, window_size

app = FastAPI(
    title="API de Previsão de Preço com LSTM",
    description="Esta API recebe os 60 últimos preços normalizados e retorna a previsão do próximo valor com uma rede neural LSTM treinada.",
    version="1.0.0"
)

# Permite chamadas de qualquer origem (ajuste se necessário)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ex: ["https://seusite.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carrega o modelo LSTM
model = load_model("modelo_lstm_dis.h5")

# Define o schema da requisição
class PriceRequest(BaseModel):
    prices: list[float]  # lista com os últimos 60 preços normalizados

# Monta arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Rota da página principal (index.html)
@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")

# Endpoint de predição
@app.post("/predict")
def predict_price(data: PriceRequest):
    if len(data.prices) != window_size:
        raise HTTPException(status_code=400, detail=f"É necessário enviar exatamente {window_size} preços.")

    try:
        X_input = preprocess_input(data.prices)
        pred_scaled = model.predict(X_input)
        pred_real = scaler.inverse_transform(pred_scaled)
        return {"previsao": float(round(pred_real[0][0], 2))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
