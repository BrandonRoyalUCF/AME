from socketIO_client import SocketIO, LoggingNamespace
import json

def on_connect(self):
    print('[Connected]')

def on_reconnect(self):
    print('[Reconnected]')

def on_disconnect(self):
    print('[Disconnected]')

def on_newMeeting(obj):
    #jsonObject = json.loads(obj)
    print(obj)
    #StartRecognition.start(obj)
    

socketIO = SocketIO('localhost', 3001, LoggingNamespace)
socketIO.on('newMeeting', on_newMeeting)
socketIO.wait(seconds=1)




