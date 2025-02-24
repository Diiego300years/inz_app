import subprocess

def list_users():
    # Pobierz listę użytkowników
    users = subprocess.run(["getent", "passwd"], capture_output=True, text=True)
    users_list = []
    if users.returncode == 0:  # Jeśli polecenie zakończyło się sukcesem
        for line in users.stdout.splitlines():
            username = line.split(":")[0]  # Użytkownik to pierwszy element
            users_list.append(username)

    result = users_list[20:]
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
    return groups_list[43:]


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
        ask_for_group = subprocess.run(["id", username], capture_output=True, text=True)
        second_result = subprocess.run(["pdbedit", "-x", username], capture_output=True, text=True)

        delete_group = subprocess.run(["groupdel", username], capture_output=True, text=True)
        if 'users' in ask_for_group.stdout:
            third_result = subprocess.run(["rm", "-rf", f"/srv/samba/public/private/{username}"],
                                          capture_output=True, text=True)
        else:
            third_result = subprocess.run(["rm", "-rf", f"/srv/samba/public/admins/{username}"],
                                          capture_output=True, text=True)

        result = subprocess.run(["userdel", "-r", username], capture_output=True, text=True)
        if result.returncode == 0 and second_result.returncode == 0 and third_result.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
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

def add_user_to_linux_group(username, group_name):
    """
    Dodaje użytkownika do grupy.
    Args:
        username (str): Nazwa użytkownika.
        group_name (str): Nazwa grupy.
    Returns:
        bool: True, jeśli operacja się powiodła, False w przeciwnym razie.
    """
    try:
        # Sprawdź, czy użytkownik istnieje
        user_check = subprocess.run(["id", username], capture_output=True, text=True)
        if user_check.returncode != 0:
            print(f"Użytkownik {username} nie istnieje.")
            return False

        # Sprawdź, czy grupa istnieje
        group_check = subprocess.run(["getent", "group", group_name], capture_output=True, text=True)
        if group_check.returncode != 0:
            print(f"Grupa {group_name} nie istnieje.")
            return False

        # Dodaj użytkownika do grupy
        result = subprocess.run(["usermod", "-aG", group_name, username], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Użytkownik {username} został pomyślnie dodany do grupy {group_name}.")
            return True
        else:
            print(f"Błąd podczas dodawania użytkownika {username} do grupy {group_name}: {result.stderr}")
            return False
    except Exception as e:
        print(f"Wystąpił wyjątek podczas dodawania użytkownika {username} do grupy {group_name}: {str(e)}")
        return False
