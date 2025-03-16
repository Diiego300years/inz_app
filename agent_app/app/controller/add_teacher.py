import os
import string
import random
import subprocess

def generate_password(length=12):
    """Generuje bezpieczne hasło."""
    characters = string.ascii_letters + string.digits
    # + string.punctuation
    set_password = ''.join(random.choice(characters) for _ in range(length))
    return set_password


def add_linux_admin(username, password):
    """Dodaje użytkownika do systemu Linux jako grupa admins oraz Samba i ustawia hasło."""
    try:
        # Dodanie użytkownika do systemu
        subprocess.run(['useradd', '-m', '-s', '/bin/bash', username], check=True)

        # Ustawienie hasła użytkownika
        subprocess.run(['chpasswd'], input=f"{username}:{password}".encode(), check=True)

        # Dodanie użytkownika do grupy `admins`
        subprocess.run(['usermod', '-aG', 'admins', username], check=True)

        subprocess.run(["smbpasswd", "-a", username], input=f"{password}\n{password}\n".encode(), check=True)

        # Tworzenie prywatnego folderu w folderze admins
        private_path = f"/srv/samba/public/admins/{username}"
        os.makedirs(private_path, exist_ok=True)
        subprocess.run(["chown", f"{username}:{username}", private_path], check=True)
        subprocess.run(["chmod", "700", private_path], check=True)

        print(f"Admin with username: {username} added with private folder: {private_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error adding admin: {e}")
        return False
