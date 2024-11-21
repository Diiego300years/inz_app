import threading
import socketio
from app.samba_scripts.samba_handle import get_active_samba_users


class SocketClient:
    def __init__(self, url, namespace=None, logger=True, engineio_logger=True):
        self.sio = socketio.Client(logger=logger, engineio_logger=engineio_logger)
        self.url = url
        self.namespace = namespace

    def connect(self):
        try:
            if self.namespace:
                self.sio.connect(self.url, namespaces=[self.namespace])
                print(f"Connected to {self.namespace}")
            else:
                self.sio.connect(self.url)
                print(f"Connected to default namespace '/'")
        except Exception as e:
            print(f"Connection error: {e}")

    def emit(self, event, data):
        try:
            if self.namespace:
                self.sio.emit(event, data, namespace=self.namespace)
                print(f"Emitted event '{event}' with data {data} to namespace {self.namespace}")
            else:
                self.sio.emit(event, data)
                print(f"Emitted event '{event}' with data {data} to default namespace '/'")
        except Exception as e:
            print(f"Emit error: {e}")

    def disconnect(self):
        self.sio.disconnect()
        print(f"Disconnected from {self.namespace or 'default namespace'}")


def send_data_to_namespace(data, url, namespace=None, event='event_name'):
    client = SocketClient(url, namespace=namespace)
    try:
        client.connect()
        client.emit(event, data)
    finally:
        client.disconnect()


# Dane do przesłania
paginated_users = 2
total_pages = 2

data_default = {
    'users': paginated_users,
    'page': 1,
    'total_pages': total_pages
}

data_edit_user = {'info': 'edit_user namespace data'}

# Parametry połączenia
url = 'http://localhost:5002'
default_event = 'update_users'
edit_user_event = 'agent_data'

# Uruchamianie funkcji w osobnych wątkach
thread1 = threading.Thread(target=send_data_to_namespace, args=(data_default, url), kwargs={'event': default_event})
thread2 = threading.Thread(target=send_data_to_namespace, args=(data_edit_user, url), kwargs={'namespace': '/user_edit', 'event': edit_user_event})

thread1.start()
thread2.start()

thread1.join()
thread2.join()
