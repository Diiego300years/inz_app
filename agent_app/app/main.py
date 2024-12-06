import time
import redis
import json
import threading
from flask import Flask, request, jsonify

from samba_scripts.add_teacher import add_linux_admin
from samba_scripts.add_user import generate_password, add_linux_user
from samba_scripts.linux_handle import get_system_usage, get_top_resource_hungry_processes
from samba_scripts.samba_handle import get_active_samba_users, get_samba_server_usage

# Konfiguracja Redis
redis_client = redis.StrictRedis(host='nrm_redis', port=6379, db=0)

# Flask app do obsługi API
app = Flask(__name__)

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

@app.route('/add_user', methods=['POST'])
def add_user():
    """API endpoint do dodania użytkownika do systemu i Samby."""
    try:
        data = request.json
        print("Otrzymane dane:", data)
        username = data.get('username')
        print("Otrzymany username:", username)
    except Exception as ex:
        print(ex)
    try:
        data = request.json
        username = data.get('username')

        if not username:
            return jsonify({"status": "error", "message": "Brak nazwy użytkownika"}), 400

        password = generate_password()  # Możesz użyć funkcji do generowania losowego hasła

        if add_linux_user(username, password):
            print("no działa")
            payload = {"username": username, "password": password}
            return jsonify({"status": "success", "data_to_copy": payload})

        else:
            return jsonify({"status": "error", "message": f"Wystąpił błąd: "}), 500


    except Exception as e:
        return jsonify({"status": "error", "message": f"Wystąpił błąd: {str(e)}"}), 500


@app.route('/add_admin', methods=['POST'])
def add_admin():
    """API endpoint do dodania admina/wykładowcy do systemu i Samby."""
    try:
        data = request.json
        username = data.get('teacher_name')
        print("UDAŁO SIĘ MAM TO", username)

        if not username:
            return jsonify({"status": "error", "message": "Brak nazwy użytkownika"}), 400

        # Generowanie hasła dla użytkownika
        password = generate_password()  # Możesz użyć funkcji do generowania losowego hasła

        if add_linux_admin(username, password):
            payload = {"username": username, "password": password}
            print("działa też?")
            return jsonify({"status": "success", "data_to_copy": payload})
        else:
            return jsonify({"status": "error", "message": f"Wystąpił błąd: "}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": f"Wystąpił błąd: {str(e)}"}), 500


def flask_thread():
    """Uruchamia aplikację Flask w osobnym wątku."""
    app.run(host='0.0.0.0', port=5005)

if __name__ == '__main__':
    # Tworzenie wątków dla każdej funkcji
    samba_thread = threading.Thread(target=publish_samba_users, daemon=True)
    server_thread = threading.Thread(target=publish_server_metrics, daemon=True)
    samba_metrics_thread = threading.Thread(target=publish_samba_metrics, daemon=True)
    most_used_processes_thread = threading.Thread(target=publish_most_used_processes, daemon=True)
    flask_api_thread = threading.Thread(target=flask_thread, daemon=True)

    # Uruchomienie wątków
    samba_thread.start()
    server_thread.start()
    samba_metrics_thread.start()
    most_used_processes_thread.start()
    flask_api_thread.start()

    # Zapewnienie działania głównego wątku
    samba_thread.join()
    server_thread.join()
    samba_metrics_thread.join()
    most_used_processes_thread.join()
    flask_api_thread.join()
