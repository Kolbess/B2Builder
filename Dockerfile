# Etap 1: Budowanie i zależności
# Pinning to "bookworm" (Debian 12 Stable) prevents the OS from changing unexpectedly
FROM python:3.10-slim-bookworm AS builder

WORKDIR /app

# Prevent interactive prompts during apt-get
ARG DEBIAN_FRONTEND=noninteractive

# Update to modern package names (-2.0-dev instead of 2.0-dev)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    pkg-config \
    libpango1.0-dev \
    libcairo2-dev \
    libgdk-pixbuf-2.0-dev \
    libffi-dev \
    shared-mime-info \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ==========================================

# Etap 2: Obraz finalny
# Pinning to "bookworm" ensures consistency with the builder stage
FROM python:3.10-slim-bookworm

WORKDIR /app

# Prevent interactive prompts during apt-get
ARG DEBIAN_FRONTEND=noninteractive

# Update to modern package names (-2.0-0 instead of 2.0-0)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libcairo2 \
    libgdk-pixbuf-2.0-0 \
    shared-mime-info \
    fonts-liberation \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Kopiowanie zainstalowanych paczek Pythona z etapu builder
COPY --from=builder /install /usr/local

# Tworzenie użytkownika nieuprzywilejowanego
RUN useradd -m b2user 

# Kopiowanie plików aplikacji od razu z odpowiednimi uprawnieniami
COPY --chown=b2user:b2user . .

USER b2user

# Port FastAPI
EXPOSE 8000

# Uruchomienie serwera Uvicorn 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]