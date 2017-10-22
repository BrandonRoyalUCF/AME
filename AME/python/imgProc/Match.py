#GitHub Code

from StartRecognition import *
import sys
import cv2
import json

 

#start = StartRecognition(jsonObject)
#finalJson = start.startRecognition()

jsonString = sys.argv[1]
jsonObject = json.loads(jsonString)
meetingPicBuffer = jsonObject['meetingPic']
#image = Image.open(io.BytesIO(meetingPicBuffer))
#image.save('test')

#cv2.startWindowThread()
#cv2.namedWindow('meetingPic')
#cv2.imshow('image', meetingPicBuffer)
#cv2.waitKey(0)
#finalJson = json.dumps(meetingPicBuffer)
sys.stdout.write('its working')

#start = StartRecognition(jsonObject)
#finalJson = start.startRecognition()
