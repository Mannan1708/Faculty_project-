FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only necessary files for production
COPY vector_api.py .
COPY faculty_meta.json .
COPY faculty_embeddings.json .

CMD uvicorn vector_api:app --host 0.0.0.0 --port ${PORT:-8000}
