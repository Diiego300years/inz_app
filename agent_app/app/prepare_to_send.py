from servers_scripts.linux_handle import get_system_usage, get_top_resource_hungry_processes
from servers_scripts.samba_handle import get_active_samba_users, get_samba_server_usage
import time
import redis
import json

# Konfiguracja Redis
redis_client = redis.StrictRedis(host='nrm_redis', port=6379, db=0)


def publish_samba_users():
    while True:
        data = get_active_samba_users()
        serialized_data = json.dumps(data)
        redis_client.set('latest_samba_metrics', serialized_data)
        redis_client.publish('samba_metrics', serialized_data)
        current_time = time.ctime()
        print(f"Published Samba Users: {data} at time: {current_time}")
        time.sleep(13)

def publish_server_metrics():
    while True:
        data = get_system_usage()
        serialized_data = json.dumps(data)
        redis_client.set('latest_server_metrics', serialized_data)
        redis_client.publish('server_metrics', serialized_data)
        current_time = time.ctime()
        print(f"Published Server Metrics: {data} at time: {current_time}")
        time.sleep(13)

def publish_samba_metrics():
    while True:
        data = get_samba_server_usage()
        serialized_data = json.dumps(data)
        redis_client.set('latest_samba_server_metrics', serialized_data)
        redis_client.publish('samba_server_metrics', serialized_data)
        current_time = time.ctime()
        print(f"Published Samba Server Usage: {data} at time: {current_time}")
        time.sleep(13)

def publish_most_used_processes():
    while True:
        data = get_top_resource_hungry_processes()
        serialized_data = json.dumps(data)
        redis_client.set('latest_most_used_processes', serialized_data)
        redis_client.publish('most_used_processes', serialized_data)
        current_time = time.ctime()
        print(f"Published Most Used Processes: {data} at time: {current_time}")
        time.sleep(13)

