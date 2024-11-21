import socketio

class DashboardNamespaceClient:
    """
    /agent is a place for dashboard information station
    """
    def __init__(self, url, namespace='/agent', event='agent_data', logger=True, engineio_logger=True):
        self.sio = socketio.Client(logger=logger, engineio_logger=engineio_logger)
        self.url = url
        self.namespace = namespace
        self.event = event

    def connect(self):
        try:
            if not self.sio.connected:
                self.sio.connect(self.url, namespaces=[self.namespace])
            print(f"Connected to dashboard agent namespace '{self.namespace}'")
        except Exception as e:
            print(f"Connection error to '{self.namespace}': {e}")

    def emit(self, data):
        try:
            print("I try sent data", data)
            self.sio.emit(self.event, data, namespace=self.namespace)
            print(f"Emitted event '{self.event}' with data {data} to namespace '{self.namespace}'")

        except Exception as e:
            print(f"Emit error to '{self.namespace}': {e}")

    def disconnect(self):
        self.sio.disconnect()
        print(f"Disconnected from default namespace '{self.namespace}'")

    def send_data(self, data):
        try:
            self.connect()
            self.emit(data)
        finally:
            self.disconnect()
