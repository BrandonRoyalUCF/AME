#GitHub Code

from StartRecognition import *
import sys
import cv2
import json
import pybase64
from pymongo import *
from bson.objectid import ObjectId
from PIL import Image
import io
 

#start = StartRecognition(jsonObject)
#finalJson = start.startRecognition()


#Get the Json String Passed in from the Node and load it
jsonString = sys.argv[1]
jsonObject = json.loads(jsonString)


#items from the json String
meeting_id = jsonObject['meeting_id'] #object id string
#student_ids = jsonObject['student_ids'] #array of object id strings
sys.stdout.write(meeting_id)
#Connect to the database and get the meeting pic buffer based off the meeting id
client = MongoClient('mongodb://localhost:27017/')
db = client['test']

#first get the meeting picture from the database and store it locally
meetings = db['meetings']
newMeeting = meetings.find_one({"_id": ObjectId(meeting_id)})

sys.stdout.write(meeting_id)

meetingPicBuffer = newMeeting['meetingPic']
directory = 'C://AmeTesting//' + meeting_id
os.makedirs(directory)
pathMeetingPic = directory + '//' + meeting_id + '.png'
image = Image.open(io.BytesIO(meetingPicBuffer))
image.save(pathMeetingPic)

sys.stdout.write(pathMeetingPic)

#now for each student in the class, get their individual pictures and store them locally

#students = db['students']
arrayOfStudentPicPaths = []
#for student_id in student_ids:
#    student = students.find_one({"_id": student_id})
    
#    path = 'C://AmeTesting//studentPics//' + student_id +'.png'
    #arrayOfStudentPicPaths.append(path)
#    studentPortraitBuffer = student['studentPortrait']
    
#    image = Image.open(io.BytesIO(studentPortraitBuffer))
#    image.save(path)
    
start = StartRecognition(student_ids, meeting_id, pathMeetingPic, arrayOfStudentPicPaths, directory)
finalJson = start.startRecognition()

sys.stdout.write(finalJson)

#image = Image.open(io.BytesIO(meetingPicBuffer))
#image.save('test')

#cv2.startWindowThread()
#cv2.namedWindow('meetingPic')
#cv2.imshow('image', meetingPicBuffer)
#cv2.waitKey(10000)
#finalJson = json.dumps(meetingPicBuffer)


#start = StartRecognition(jsonObject)
#finalJson = start.startRecognition()
