import json

def handle_users_data(data):
    try:
        if isinstance(data, str):
            users = json.loads(data)
            return users
        elif isinstance(data, list):
            users = data
            return users
        else:
            return 404
    except Exception as e:
        print(f"Błąd podczas sprawdzania Redis z samba_data: {e}")

def handle_server_data(data):
    try:
        if isinstance(data, str):
            server_data = json.loads(data)
            return server_data
        elif isinstance(data, dict):
            server_data = data
            return server_data
        else:
            print("nie działa konwersja do jsona.")
            return 404
    except Exception as e:
        print(f"Błąd podczas sprawdzania Redis z server_data: {e}")