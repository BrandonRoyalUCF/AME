from socketIO_client import SocketIO, LoggingNamespace
import json
from cv2 import imdecode
import StartRecognition

def on_connect(self):
    print('[Connected]')

def on_reconnect(self):
    print('[Reconnected]')

def on_disconnect(self):
    print('[Disconnected]')


    
jsonObject = 'test'
start = StartRecognition()
finalJson = start.startRecognition(jsonObject)

#socketIO = SocketIO('localhost', 3001, LoggingNamespace)
#socketIO.on('newMeeting', on_newMeeting)
#socketIO.wait(seconds=1)





