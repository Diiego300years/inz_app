import subprocess
import redis
import json

# Konfiguracja Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_samba_user_status():
    # Sprawdź cache w Redis
    cached_data = redis_client.get("samba_user_status")
    if cached_data:
        # Jeśli dane są w cache, odczytaj je
        print("Odczyt z cache")
        return json.loads(cached_data)

    # Wykonaj komendę smbstatus, jeśli brak cache
    result = subprocess.run(['smbstatus'], stdout=subprocess.PIPE)
    users = []
    for line in result.stdout.decode('utf-8').splitlines():
        if "User" in line:
            user_info = line.split()
            users.append({
                "name": user_info[0],
                "status": user_info[1]
            })

    # Zapisz dane w cache na 10 sekund
    redis_client.setex("samba_user_status", 10, json.dumps({"users": users}))
    print("Odczyt z Samba i zapis do cache")
    return {"users": users}

# # Główna pętla agenta
# while True:
#     user_status = get_samba_user_status()
#     # Wykonaj inne operacje na danych
#     time.sleep(1)
