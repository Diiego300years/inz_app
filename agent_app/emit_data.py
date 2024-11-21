import subprocess
import redis
import json
import time
import socketio
from main import get_samba_user_status

# Konfiguracja Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Konfiguracja Socket.IO (adres aplikacji Flask w Dockerze)
SOCKET_IO_URL = "http://inz_flask_app:5002"  # Zastąp `localhost` adresem kontenera, jeśli używasz Docker
sio = socketio.Client()

# Połącz z serwerem Flask
sio.connect(SOCKET_IO_URL)

while True:
    # Pobierz dane z Redis
    user_status = get_samba_user_status()
    user_status.update({"users": "kanapka"})
    # Wyślij dane do aplikacji Flask przez WebSocket
    sio.emit('agent_data', user_status)
    print("Dane wysłane do aplikacji Flask:", user_status)
    time.sleep(10)  # Wysyłanie co sekundę
