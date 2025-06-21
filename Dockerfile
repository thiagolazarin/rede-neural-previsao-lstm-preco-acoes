# Imagem base com Python
FROM python:3.11-slim

# Evita buffering de logs
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto para o container
COPY . /app

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta padrão do FastAPI (opcional, Railway ignora)
EXPOSE 8000

# Comando para iniciar a API (usa PORT do Railway ou 8000 localmente)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
