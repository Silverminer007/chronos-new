# ✅ 1. Schlanker Base Image mit Python
FROM python:3.11-slim

# ✅ 2. Environment-Variablen
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ✅ 3. Arbeitsverzeichnis erstellen
WORKDIR /app

# ✅ 4. Systemabhängigkeiten installieren
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ✅ 5. Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ 6. App-Code kopieren
COPY . .

# ✅ 7. Uvicorn + Gunicorn starten (über gunicorn mit uvicorn worker)
CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "60"]
