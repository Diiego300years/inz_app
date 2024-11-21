import socketio

# Utwórz instancję klienta Socket.IO
sio_default = socketio.Client()
sio_edit_user = socketio.Client(logger=True, engineio_logger=True)

# Obsługa zdarzeń dla namespace "/"
@sio_default.event
def connect():
    print("Connected to namespace '/'")

@sio_default.event
def disconnect():
    print("Disconnected from namespace '/'")

@sio_default.event
def response(data):
    print(f"Response from namespace '/': {data}")

# Obsługa zdarzeń dla namespace "/edit_user"
@sio_edit_user.event
def connect():
    print("Connected to namespace '/edit_user'")

@sio_edit_user.event
def disconnect():
    print("Disconnected from namespace '/edit_user'")

@sio_edit_user.event
def response(data):
    print(f"Response from namespace '/edit_user': {data}")

# Funkcja wysyłająca wiadomości do namespace "/"
def send_message_to_default():
    print("Sending message to '/'")
    sio_default.connect('http://localhost:5002/')
    sio_default.send("Hello, WebSocket from '/'!")
    sio_default.disconnect()

# Funkcja wysyłająca wiadomości do namespace "/edit_user"
def send_message_to_edit_user():
    print("Sending message to '/edit_user'")
    sio_edit_user.connect('http://localhost:5002', namespaces=['/edit_user'])
    sio_edit_user.emit('agent_data', "Hello from /edit_user!", namespace='/edit_user')
    sio_edit_user.disconnect()

# Wywołanie głównych funkcji
if __name__ == '__main__':
    send_message_to_default()  # Wysyła dane do "/"
    # send_message_to_edit_user()  # Wysyła dane do "/edit_user"
