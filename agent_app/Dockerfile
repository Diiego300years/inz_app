# Wybór oficjalnego obrazu Redis
FROM redis:7.0

# Skopiowanie niestandardowego pliku konfiguracyjnego Redis (jeśli potrzebny)
# COPY redis.conf /usr/local/etc/redis/redis.conf

# Ustawienie domyślnego polecenia uruchamiającego Redis
# Domyślnie Redis uruchamia się na porcie 6379
CMD ["redis-server"]

# Eksponowanie portu Redis
EXPOSE 6379
