import os
import string
import random
import subprocess

def add_linux_admin(username, password):
    """Dodaje użytkownika do systemu Linux i ustawia hasło."""
    try:
        # Dodanie użytkownika do systemu
        subprocess.run(['useradd', '-m', '-s', '/bin/bash', username], check=True)

        # Ustawienie hasła użytkownika
        subprocess.run(['chpasswd'], input=f"{username}:{password}".encode(), check=True)

        # Dodanie użytkownika do grupy `users`
        subprocess.run(['usermod', '-aG', 'admins', username], check=True)

        subprocess.run(["smbpasswd", "-a", username], input=f"{password}\n{password}\n".encode(), check=True)

        private_path = f"/srv/samba/private/{username}"
        os.makedirs(private_path, exist_ok=True)
        subprocess.run(["chown", f"{username}:{username}", private_path], check=True)
        subprocess.run(["chmod", "700", private_path], check=True)

        print(f"Admin with username: {username} added with private folder: {private_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error adding admin: {e}")


def add_samba_admin(username, password):
    """Dodaje użytkownika do Samby."""
    try:
        # Dodanie użytkownika do bazy Samby
        subprocess.run(['sudo', 'smbpasswd', '-a', username], input=f"{password}\n{password}\n".encode(), check=True)
        print(f"User {username} added to Samba.")
    except subprocess.CalledProcessError as e:
        print(f"Error adding Samba user: {e}")


