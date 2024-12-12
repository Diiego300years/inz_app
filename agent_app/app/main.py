import threading
from flask import Flask, request, jsonify
from .linux_scripts.users_operations import list_users, list_groups, delete_user_and_folder
from .prepare_to_send import (publish_samba_users, publish_server_metrics, publish_samba_metrics,
                             publish_most_used_processes)
from .samba_scripts.add_teacher import add_linux_admin
from .samba_scripts.add_user import generate_password, add_linux_user

# Flask app do obsługi API
app = Flask(__name__)



# DODAJ TUTAJ TOKENIZACJE JAKĄŚ PRZY CURLACH ŻEBY PODAWAĆ
#DODAJ Z SAMBĄ ABY FOLDERY SIĘ KRYLY HIDDENFOLDERS.
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


@app.route('/available_users', methods=['POST'])
def available_users():
    """Endpoint wysyłający listę użytkowników Samby oraz grup."""
    try:
        users_list = list_users()
        groups_list = list_groups()

        response = {
            "status": "success",
            "users": users_list,
            "groups": groups_list
        }
        print(f"Wysyłam użytkowników i grupy: {response}")
        return jsonify(response), 200


    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/remove_with_folder', methods=['POST'])
def remove_with_folder():
    """Endpoint do usuwania użytkownika i jego folderu."""
    try:
        data = request.json
        username = data.get('username')

        if not username:
            return jsonify({"status": "error", "message": "Brak nazwy użytkownika"}), 400

        # Tutaj wywołaj funkcję usuwającą użytkownika i jego folder, np.:
        if delete_user_and_folder(username):
            return jsonify({"status": "success", "message": f"Użytkownik {username} usunięty z folderem"}), 200
        else:
            return jsonify({"status": "error", "message": "Niemożliwe do wykonania"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/remove_without_folder', methods=['POST'])
def remove_without_folder():
    """Endpoint do usuwania użytkownika bez folderu."""
    try:
        data = request.json
        username = data.get('username')

        if not username:
            return jsonify({"status": "error", "message": "Brak nazwy użytkownika"}), 400

        # Tutaj wywołaj funkcję usuwającą użytkownika bez usuwania folderu, np.:
        print(f"Usuwam użytkownika {username} bez folderu.")
        # delete_user(username)

        return jsonify({"status": "success", "message": f"Użytkownik {username} usunięty bez folderu"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500



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
