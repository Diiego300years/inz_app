import time
import redis
import json
import random

# Konfiguracja Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


# def collect_server_metrics():
#     # Sprawdzanie połączenia z Redis
#     try:
#         redis_client.ping()
#         print("Connected to Redis")
#     except redis.exceptions.ConnectionError as e:
#         print(f"Failed to connect to Redis: {e}")
#         exit(1)
#
#     while True:
#         # Symulacja danych serwera
#         data = {
#             "cpu": random.randint(10, 90),  # Losowy poziom CPU
#             "memory": random.randint(20, 80),  # Losowy poziom pamięci
#             "disk": random.randint(30, 70)  # Losowy poziom dysku
#         }
#
#         # Publikowanie danych do Redis
#         try:
#             redis_client.set("latest_server_metrics", json.dumps(data))
#             print(f"Published data to Redis: {data}")
#         except redis.exceptions.ConnectionError as e:
#             print(f"Failed to publish to Redis: {e}")
#
#         # Odczekanie przed kolejnym cyklem
#         time.sleep(random.randint(10, 15))

def publish_server_metrics():
    while True:
        # Symulacja danych
        data = {
            "cpu": random.randint(10, 90),
            "memory": random.randint(10, 90),
            "disk": random.randint(10, 90)
        }
        redis_client.set('latest_server_metrics', json.dumps(data))
        redis_client.publish('server_metrics', json.dumps(data))
        print(f"Published: {data}")
        time.sleep(13)  # Co 10 sekund

if __name__ == '__main__':
    publish_server_metrics()

