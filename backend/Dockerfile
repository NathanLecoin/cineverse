FROM python:3.12-slim

WORKDIR /app

# Installer les dépendances système pour PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

# Copier le script d'initialisation
COPY entrypoint.sh .

# Exposer le port
EXPOSE 8000

# Commande par défaut
CMD ["bash", "entrypoint.sh"]
