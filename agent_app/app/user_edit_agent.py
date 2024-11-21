import socketio


class EditUserNamespaceClient:
    def __init__(self, url, namespace='/user_edit', event='user_edit_agent_data', logger=True, engineio_logger=True):
        self.sio = socketio.Client(logger=logger, engineio_logger=engineio_logger)
        self.url = url
        self.namespace = namespace
        self.event = event

    def connect(self):
        try:
            self.sio.connect(self.url, namespaces=[self.namespace])
            print(f"Connected to namespace '{self.namespace}'")
        except Exception as e:
            print(f"Connection error to '{self.namespace}': {e}")

    def emit(self, data):
        try:
            self.sio.emit(self.event, data, namespace=self.namespace)
            print(f"Emitted event '{self.event}' with data {data} to namespace '{self.namespace}'")
        except Exception as e:
            print(f"Emit error to '{self.namespace}': {e}")

    def disconnect(self):
        self.sio.disconnect()
        print(f"Disconnected from namespace '{self.namespace}'")

    def send_data(self, data):
        try:
            self.connect()
            self.emit(data)
        finally:
            self.disconnect()
