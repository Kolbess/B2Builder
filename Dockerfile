# Etap 1: Budowanie i zależności
FROM python:3.10-slim AS builder

WORKDIR /app

# Instalacja zależności systemowych dla WeasyPrint i kompilacji
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libpango1.0-dev \
    libcairo2-dev \
    libgdk-pixbuf2.0-dev \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Etap 2: Obraz finalny
FROM python:3.10-slim

WORKDIR /app

# Instalacja tylko niezbędnych bibliotek uruchomieniowych dla WeasyPrint
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libshared-mime-info-tracker \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Kopiowanie zainstalowanych paczek Pythona z etapu builder
COPY --from=builder /install /usr/local
COPY . .

# Tworzenie użytkownika nieuprzywilejowanego dla bezpieczeństwa
RUN useradd -m b2user && chown -R b2user /app
USER b2user

# Port FastAPI
EXPOSE 8000

# Uruchomienie serwera Uvicorn 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
