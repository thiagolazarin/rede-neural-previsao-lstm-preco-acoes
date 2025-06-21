import numpy as np
import joblib

# Parâmetros fixos
window_size = 60

# Carrega o scaler treinado do notebook
scaler = joblib.load('scaler.save')

def preprocess_input(prices: list[float]):
    """
    prices: lista de 60 preços em escala real
    Retorna: array formatado para entrada no LSTM
    """
    prices = np.array(prices).reshape(-1, 1)
    scaled = scaler.transform(prices)
    X = scaled.reshape(1, window_size, 1)
    return X
