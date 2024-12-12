import subprocess

def list_users():
    # Pobierz listę użytkowników
    users = subprocess.run(["getent", "passwd"], capture_output=True, text=True)
    users_list = []
    if users.returncode == 0:  # Jeśli polecenie zakończyło się sukcesem
        for line in users.stdout.splitlines():
            username = line.split(":")[0]  # Użytkownik to pierwszy element
            users_list.append(username)

    result = users_list[18:]
    return result

def list_groups():
    groups = subprocess.run(["getent", "group"], capture_output=True, text=True)
    groups_list = []
    if groups.returncode == 0:  # Jeśli polecenie zakończyło się sukcesem
        for line in groups.stdout.splitlines():
            group_name = line.split(":")[0]  # Grupa to pierwszy element
            if not group_name.isdigit():
                groups_list.append(group_name)
    groups_list.append('users')
    return groups_list[42:]


def delete_user_and_folder(username):
    """
    Usuwa użytkownika i jego katalog domowy.
    Args:
        username (str): Nazwa użytkownika do usunięcia.
    Returns:
        bool: True, jeśli operacja się powiodła, False w przeciwnym razie.
    """
    try:
        # Usuwanie użytkownika i katalogu domowego
        result = subprocess.run(["userdel", "-r", username], capture_output=True, text=True)
        second_result = subprocess.run(["pdbedit", "-x", username], capture_output=True, text=True)
        third_result = subprocess.run(["rm", "-rf", f"/srv/samba/private/{username}"], capture_output=True, text=True)
        if result.returncode == 0 and second_result.returncode == 0 and third_result.returncode == 0:
            print(f"Użytkownik {username} został pomyślnie usunięty wraz z folderem.")
            return True
        else:
            print(f"Błąd podczas usuwania użytkownika {username}: {result.stderr}")
            return False
    except Exception as e:
        print(f"Wystąpił wyjątek podczas usuwania użytkownika {username}: {str(e)}")
        return False

def delete_user_without_folder(username):
    """
    Usuwa użytkownika i jego katalog domowy.
    Args:
        username (str): Nazwa użytkownika do usunięcia.
    Returns:
        bool: True, jeśli operacja się powiodła, False w przeciwnym razie.
    """
    try:
        # Usuwanie użytkownika i katalogu domowego
        result = subprocess.run(["userdel", "-r", username], capture_output=True, text=True)
        second_result = subprocess.run(["pdbedit", "-x", username], capture_output=True, text=True)
        if result.returncode == 0 and second_result.returncode == 0:
            print(f"Użytkownik {username} został pomyślnie usunięty bez folderu.")
            return True
        else:
            print(f"Błąd podczas usuwania użytkownika {username}: {result.stderr}")
            return False
    except Exception as e:
        print(f"Wystąpił wyjątek podczas usuwania użytkownika {username}: {str(e)}")
        return False
