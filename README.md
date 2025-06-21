# API de Previsão de Preço de Ações com LSTM

Este projeto implementa um modelo de redes neurais LSTM para prever o preço de fechamento de ações da empresa Yahoo Finance, usando dados históricos.

## Como rodar com Docker

```bash
docker build -t lstm-api .
docker run -d -p 8000:8000 lstm-api
