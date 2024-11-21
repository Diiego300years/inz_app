#!/bin/bash

# Uruchomienie Samby
echo "Starting Samba service..."
service smbd start || { echo "Failed to start Samba"; exit 1; }

# Dodanie użytkownika systemowego (jeśli nie istnieje)
if ! id -u sambauser > /dev/null 2>&1; then
    echo "Adding system user sambauser..."
    useradd -M sambauser || { echo "Failed to add system user sambauser"; exit 1; }
fi

# Dodanie użytkownika Samby
echo "Adding Samba user..."
(echo "sambauser"; echo "sambauser") | smbpasswd -s -a sambauser || { echo "Failed to add Samba user"; exit 1; }

# Uruchomienie aplikacji Python
echo "Starting Python application..."
exec python /app/app/main_tasks.py || { echo "Failed to start Python application"; exit 1; }
