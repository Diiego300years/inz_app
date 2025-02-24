from multiprocessing import Process
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from prepare_to_send import (publish_samba_users, publish_server_metrics, publish_samba_metrics,
                             publish_most_used_processes)
from controller.users_operations import list_users, list_groups, delete_user_and_folder, add_user_to_linux_group
from controller.add_teacher import add_linux_admin
from controller.add_user import generate_password, add_linux_user

# Flask app do obsługi API
app = Flask(__name__)

# Konfiguracja JWT
app.config["JWT_SECRET_KEY"] = "twoj_sekretny_klucz"  # Ustaw tutaj bezpieczny klucz
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    """Endpoint do logowania i generowania tokenu."""
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Walidacja poprawności.
    if username == "admin" and password == "admin123":
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Nieprawidłowe dane logowania"}), 401

@app.route('/add_user', methods=['POST'])
@jwt_required()
def add_user():
    """API endpoint for add user to Linux system & Samba."""
    try:
        data = request.json
        username = data.get('username')

        if not username:
            return jsonify({"status": "error", "message": "Brak nazwy użytkownika"}), 400

        password = generate_password()

        if add_linux_user(username, password):
            payload = {"username": username, "password": password}
            return jsonify({"status": "success", "data_to_copy": payload})

        else:
            return jsonify({"status": "error", "message": f"Wystąpił błąd: "}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": f"Wystąpił błąd: {str(e)}"}), 500


@app.route('/add_admin', methods=['POST'])
@jwt_required()
def add_admin():
    """API endpoint do dodania admina/wykładowcy do systemu i Samby."""
    try:
        data = request.json
        username = data.get('teacher_name')

        if not username:
            return jsonify({"status": "error", "message": "Brak nazwy użytkownika"}), 400

        # Generowanie hasła dla użytkownika
        password = generate_password()

        if add_linux_admin(username, password):
            payload = {"username": username, "password": password}
            return jsonify({"status": "success", "data_to_copy": payload})
        else:
            return jsonify({"status": "error", "message": f"Wystąpił błąd: "}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": f"Wystąpił błąd: {str(e)}"}), 500


@app.route('/available_users', methods=['POST'])
@jwt_required()
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
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/remove_with_folder', methods=['POST'])
@jwt_required()
def remove_with_folder():
    """Endpoint do usuwania użytkownika i jego folderu."""
    try:
        data = request.json
        username = data.get('username')

        if not username:
            return jsonify({"status": "error", "message": "Brak nazwy użytkownika"}), 400

        if delete_user_and_folder(username):
            return jsonify({"status": "success", "message": f"Użytkownik {username} usunięty z folderem"}), 200
        else:
            return jsonify({"status": "error", "message": "Niemożliwe do wykonania"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/remove_without_folder', methods=['POST'])
@jwt_required()
def remove_without_folder():
    """Endpoint do usuwania użytkownika bez folderu."""
    try:
        data = request.json
        username = data.get('username')

        if not username:
            return jsonify({"status": "error", "message": "Brak nazwy użytkownika"}), 400

        return jsonify({"status": "success", "message": f"Użytkownik {username} usunięty bez folderu"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/add_user_to_group', methods=['POST'])
@jwt_required()
def add_user_to_group():
    """Endpoint do dodawania użytkownika do grupy w systemie."""
    try:

        data = request.json
        username = data.get('username')
        group_name = data.get('group')
        print(f"Received request: username={username}, group_name={group_name}")  # DEBUG

        if not username or not group_name:
            print('username and group_name are required')
            return jsonify({"status": "error", "message": "Brak nazwy użytkownika lub grupy"}), 400

        # Wywołaj funkcję add_user_to_group zdefiniowaną wcześniej
        success = add_user_to_linux_group(username, group_name)

        if success:
            return jsonify({"status": "success", "message": f"Użytkownik {username} został dodany do grupy {group_name}."}), 200
        else:
            return jsonify({"status": "error", "message": f"Nie udało się dodać użytkownika {username} do grupy {group_name}."}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": f"Wystąpił błąd: {str(e)}"}), 500


def flask_process():
    """Uruchamia aplikację Flask w osobnym procesie."""
    app.run(host='0.0.0.0', port=5005)


def start_tasks():
    """Uruchamia zadania w osobnym procesie."""
    tasks = [
        publish_samba_users,
        publish_server_metrics,
        publish_samba_metrics,
        publish_most_used_processes
    ]
    for task in tasks:
        process = Process(target=task)
        process.start()



if __name__ == '__main__':
    # Tworzenie procesu Flask
    flask_proc = Process(target=flask_process)
    flask_proc.start()  # Flask działa w osobnym procesie

    # Uruchamianie zadań (każde zadanie w swoim procesie)
    start_tasks()

    # Czekanie na zakończenie procesu Flask (jeśli konieczne)
    flask_proc.join()
