#!/bin/bash
# Instalacja samba oraz nano podczas konieczności ręcznej poprawy konfiguracji.
apt update;
apt install samba -y;
apt install nano -y;

# Konfiguracja Samba.
cat /etc/samba/smb.conf
echo "" > /etc/samba/smb.conf
cp /app/server_setup/smb.conf /etc/samba/

# Tworzenie zmiennych katalogów głównych
BASE_DIR="/srv/samba/"
PUBLIC_DIR="$BASE_DIR/public"
ADMINS_DIR="$BASE_DIR/public/admins"
PRIVATE_DIR="$BASE_DIR/public/private"

groupadd admins;
groupadd users;


# R rekuencyjne
# chmod jest zbędny
mkdir -p $PUBLIC_DIR $ADMINS_DIR $PRIVATE_DIR;
echo "stworzono foldery"

# Właścieciel root ale pełne uprawnienia posiada również grupa admins.
chown root $BASE_DIR
echo "Nadawanie uprawnień..."
setfacl -m g:admins:rx $BASE_DIR
setfacl -m g:users:--x $BASE_DIR

# Ustawienia dla "public".
chown root $PUBLIC_DIR
setfacl -m g:admins:rx $PUBLIC_DIR
setfacl -m g:users:rx $PUBLIC_DIR

# Ustawienia dla "admins"
chown root $ADMINS_DIR
setfacl -m g:admins:rx $ADMINS_DIR

# Ustawienia dla "private"
setfacl -m g:admins:rx $PRIVATE_DIR
setfacl -m g:users:rx $PRIVATE_DIR

service smbd start;

# poniżej wrzucam dla działania CMD w ENTRYPOINT
exec "$@"

