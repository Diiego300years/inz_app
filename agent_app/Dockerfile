# Wybór obrazu bazowego z Pythonem
FROM python:3.10-slim

# Ustawienie zmiennych środowiskowych
ENV DEBIAN_FRONTEND=noninteractive

# Instalacja niezbędnych pakietów i Samby
RUN apt-get update && apt-get install -y \
    samba \
    samba-common-bin \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Tworzenie katalogu roboczego dla aplikacji
WORKDIR /app

# Skopiowanie plików aplikacji
COPY . /app
COPY requirements.txt /app/requirements.txt

# Instalacja zależności Pythona
RUN pip install --no-cache-dir -r requirements.txt

# Konfiguracja Samby
RUN mkdir -p /samba/share && \
    echo -e "[global]\n\
workgroup = WORKGROUP\n\
security = user\n\
map to guest = Bad User\n\
\n\
[sambashare]\n\
path = /samba/share\n\
browsable = yes\n\
writable = yes\n\
guest ok = yes\n\
read only = no" > /etc/samba/smb.conf && \
    chmod -R 777 /samba/share

# Eksponowanie portów Samby
EXPOSE 137 138 139 445

# Dodawanie użytkownika Samby przy starcie kontenera
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Punkt wejściowy
ENTRYPOINT ["/entrypoint.sh"]
