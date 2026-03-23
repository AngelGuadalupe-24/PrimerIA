FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# Instalar numpy compatible con Python 3.11
RUN pip install --no-cache-dir numpy==1.26.4

# Instalar spacy compatible con Python 3.11
RUN pip install --no-cache-dir spacy==3.6.1

# Instalar el resto de librerías
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]