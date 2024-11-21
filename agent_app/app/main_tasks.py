import threading
from samba_scripts.samba_handle import get_active_samba_users
from dashboard_agent import DashboardNamespaceClient
from user_edit_agent import EditUserNamespaceClient
import time


# Dane do przesłania
paginated_users = 2
total_pages = 2


def update_system_info():

    previous_users = []
    previous_server_data = []
    per_page = 2

    users = get_active_samba_users()

    if users != previous_users:
        total_pages = (len(users) + per_page - 1) // per_page
        splitted_users = [user.split() for user in users]
        paginated_users = splitted_users[:per_page]

        data_default = {
            'users': ["marcin", "heniek", "Kasia"],
            'page': 1,
            'total_pages': total_pages
        }

        try:
            return data_default
        except Exception as e:
            print(e)
            return []



data_default = {
    'users': paginated_users,
    'page': 1,
    'total_pages': total_pages
}

data_default = update_system_info()

data_edit_user = {'info': 'edit_user namespace data'}

# URL serwera
url = 'http://localhost:5002'

def keep_sending_default_data(agent, data):
    """Funkcja w wątku wysyłająca dane dla dashboardu."""
    try:
        while True:
            agent.emit(data)
            time.sleep(10)  # Wysyłanie danych co 10 sekund
    except KeyboardInterrupt:
        agent.disconnect()

def keep_sending_edit_user_data(agent, data):
    """Funkcja w wątku wysyłająca dane dla edycji użytkownika."""
    try:
        while True:
            agent.emit(data)
            time.sleep(10)
    except KeyboardInterrupt:
        agent.disconnect()

if __name__ == "__main__":
    # Tworzenie agentów
    dashboard_agent = DashboardNamespaceClient(url)
    user_edit_agent = EditUserNamespaceClient(url)

    # Łączenie agentów
    dashboard_agent.connect()
    user_edit_agent.connect()

    # Uruchamianie wątków
    thread1 = threading.Thread(target=keep_sending_default_data, args=(dashboard_agent, data_default))
    thread2 = threading.Thread(target=keep_sending_edit_user_data, args=(user_edit_agent, data_edit_user))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
