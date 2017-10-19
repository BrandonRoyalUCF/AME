from StartRecognition import *
import sys
import cv2
import json

jsonString = sys.argv[1]
#start = StartRecognition(jsonObject)
#finalJson = start.startRecognition()

jsonObject = json.loads(jsonString)

meetingPic = jsonObject['meetingPic']

sys.stdout.write(jsonString)