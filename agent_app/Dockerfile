# Bazowy obraz Python
FROM python:3.10-slim

# Tworzenie katalogu aplikacji
WORKDIR /app

# Kopiowanie pliku wymagań i instalacja zależności
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie aplikacji
COPY . /app

# Punkt startowy kontenera
ENTRYPOINT ["python", "./app/main.py"]
