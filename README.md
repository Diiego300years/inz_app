Cześć,
stworzyłem aplikację do zarządzania serwerem plików Samba oraz Linux. Aplikacja potrafi monitorować co się dzieje na serwerze, dodawać/usuwać użytkowników/administratorów Samba, czy dodawać ich do oddzielnych grup. Aplikacja jest w całości skonteneryzowana.  

Aplikacja zawiera kilka kluczowych implementacji:
- podejście agent-aplikacja. Agent jest w postaci API oraz kilku osobnych funkcji mierzących metryki w tle. Aplikacja typu SSR w folderze nrm_app odpowiada za zwracanie odpowiednich widoków,  
- podejście publish/subscribe. Dane zbierane przez agenta odnośnie serwera Linux działają w różnych od siebie procesach co odciąża serwer. Następie zapisują metryki do serwera REDIS i są odbierane przez główną aplikację SSR,
- wykorzystanie WebSockets do zwrócenia danych w dashboard w nrm_app. Dzięki nasłuchiwaniu redis w przypadku zmian, wysyłana jest informacja do klienta z najnowszymi informacjami. 

W celu uruchomienia należy podmienić nazwę .env.sample na .env. Następnie będąc na wysokości docker-compose agent_app uruchamiamy docker compose up --build, to samo w nrm_app. Aplikacja jest dostępna w localhost:5002


<img width="518" alt="image" src="https://github.com/user-attachments/assets/ddfae63a-a8a4-4029-8602-a537d91d9482" />

Zrzut ekranu strony głównej.
Źródło: opracowanie własne.


<img width="440" alt="image" src="https://github.com/user-attachments/assets/66f86d20-80b3-4c54-b93f-26beb71b250d" />

Rys. 18 Zrzut ekranu strony podglądu i edycji użytkownika.
Źródło: opracowanie własne.
