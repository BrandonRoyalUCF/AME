from socketIO_client import SocketIO, LoggingNamespace



def on_connect(self):
    print('[Connected]')

def on_reconnect(self):
    print('[Reconnected]')

def on_disconnect(self):
    print('[Disconnected]')

def on_custom(data):
    print(data)


socketIO = SocketIO('localhost', 3001, LoggingNamespace)
socketIO.on('custom', on_custom)
socketIO.wait(seconds=1)