# app/extensions.py
from flask_socketio import SocketIO

socketio = SocketIO(async_mode='gevent', cors_allowed_origins="*", logger=True, engineio_logger=True)
