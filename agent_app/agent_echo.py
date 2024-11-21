import time
import socketio

from app.main_tasks import data_default
from app.samba_scripts.samba_handle import get_active_samba_users

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to the server!")

@sio.event
def disconnect():
    print("Disconnected from the server!")

@sio.event
def response(data):
    print(f"Response from server: {data}")

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
            'users': paginated_users,
            'page': 1,
            'total_pages': total_pages
        }

        try:
            return data_default
        except Exception as e:
            print(e)
            return []
    else:
        return []


def start_background_task():
    while True:
        update_system_info()
        time.sleep(10)


if __name__ == '__main__':
    start_background_task()
