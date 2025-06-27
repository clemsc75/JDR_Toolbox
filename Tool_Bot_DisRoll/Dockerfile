# Utiliser une image Python officielle
FROM --platform=linux/arm64 python:3.11-slim


# Définir le répertoire de travail
WORKDIR /app

# Copier le script et le fichier de requirements
COPY requirements.txt /app
COPY Bot_DisRoll.py /app


# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exécuter le script Python
CMD ["python", "Bot_DisRoll.py"]
