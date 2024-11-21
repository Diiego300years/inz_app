import socketio

sio = socketio.Client(logger=True, engineio_logger=True)

try:
    sio.connect('http://localhost:5002', namespaces=['/user_edit'])
    print("Connected to /user_edit")
    sio.emit('agent_data', {'info': 'Test data'}, namespace='/user_edit')
    print("Data sent to /user_edit")
finally:
    sio.disconnect()