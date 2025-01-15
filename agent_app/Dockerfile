# Bazowy obraz Python
FROM python:3.10-slim

# Instalacja podstawowych pakietów systemowych i ACL
RUN apt-get update && apt-get install -y --no-install-recommends \
    acl \
    dbus \
    && rm -rf /var/lib/apt/lists/*

# Tworzenie katalogu aplikacji
WORKDIR /app

# Kopiowanie aplikacji
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Punkt startowy kontenera
CMD ["python", "./app/main.py"]
