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
cv2.imshow('image', meetingPicBuffer)
finalJson = json.dumps(meetingPicBuffer)
sys.stdout.write(finalJson)

#start = StartRecognition(jsonObject)
#finalJson = start.startRecognition()
