from StartRecognition import *
import sys

jsonObject = sys.argv[1]
start = StartRecognition(jsonObject)
finalJson = start.startRecognition()


