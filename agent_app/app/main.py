import time
import redis
import json
from samba_scripts.linux_handle import get_system_usage, get_top_resource_hungry_processes
from samba_scripts.samba_handle import get_active_samba_users, get_samba_server_usage
import threading

# Konfiguracja Redis
redis_client = redis.StrictRedis(host='nrm_redis', port=6379, db=0)

def publish_samba_users():
    while True:
        data = get_active_samba_users()
        serialized_data = json.dumps(data)
        redis_client.set('latest_samba_metrics', serialized_data)
        redis_client.publish('samba_metrics', serialized_data)
        current_time = time.ctime()
        print(f"Published: {data} at time: ", current_time)
        time.sleep(13)

def publish_server_metrics():
    while True:
        data = get_system_usage()
        serialized_data = json.dumps(data)
        redis_client.set('latest_server_metrics', serialized_data)
        redis_client.publish('server_metrics', serialized_data)
        current_time = time.ctime()
        print(f"Published: {data} at time: ", current_time)
        time.sleep(13)

def publish_samba_metrics():
    while True:
        data = get_samba_server_usage()
        print(data.values())
        print("TYP TEGGGGO TO ", type(data))
        serialized_data = json.dumps(data)
        print("DATAAAAAA" , data, "SERIALIZED DATAAAAA", serialized_data, "samba server usage", type(serialized_data))
        redis_client.set('latest_samba_server_metrics', serialized_data)
        redis_client.publish('samba_server_metrics', serialized_data)
        current_time = time.ctime()
        print(f"Published: {data} at time: ", current_time)
        time.sleep(13)

def publish_most_used_processes():
    while True:
        data = get_top_resource_hungry_processes()
        serialized_data = json.dumps(data)
        redis_client.set('latest_most_used_processes', serialized_data)
        redis_client.publish('most_used_processes', serialized_data)
        current_time = time.ctime()
        print(f"Published: {data} at time: ", current_time)
        time.sleep(13)

if __name__ == '__main__':
    # Tworzenie wątków dla każdej funkcji
    samba_thread = threading.Thread(target=publish_samba_users, daemon=True)
    server_thread = threading.Thread(target=publish_server_metrics, daemon=True)
    samba_metrics_thread = threading.Thread(target=publish_samba_metrics, daemon=True)
    most_used_processes_thread = threading.Thread(target=publish_most_used_processes, daemon=True)

    # Uruchomienie wątków
    samba_thread.start()
    server_thread.start()
    samba_metrics_thread.start()
    most_used_processes_thread.start()

    # Zapewnienie działania głównego wątku
    samba_thread.join()
    server_thread.join()
    samba_metrics_thread.join()
    most_used_processes_thread.join()

