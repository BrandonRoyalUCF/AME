#############################################################################################################################
# Authors: Brandon Royal, Stephen Ulmer, Vien Yeung         
# 
# Description: Main Entry Point for Application
# 
# Change Log:
#   - Brandon Royal - Initial
#
#############################################################################################################################


#from StartRecognition import *
#from DepthData import *
import sys
import cv2
import json
import pybase64
from pymongo import *
from bson.objectid import ObjectId
from PIL import Image
import io
from DataBase import *
from Meeting import *
import os
from StartProcessing import *

#hardcode in current mode to decide which kind of test is being ran
#FullTest, DepthDataTest, MatchingAndSocialTest
mode = "FullTest" 

#########################################################
# Partial Testing Block Entry
#########################################################

if(mode == "MatchingAndSocialTest"):
    #matching testing
    start = StartRecognition(1,2,3,4,5)
    start.testMatching()

if(mode == "DepthDataTest"):
    #depth data testing
    start = DepthData("original.jpg", "depth.jpg")

    fakeSocialMatrix = []
    fakeSocialMatrix.append([0, 5, 22, 33, 223])
    fakeSocialMatrix.append([5, 0, 36, 27, 12])
    fakeSocialMatrix.append([22, 36, 0, 40, 345])
    fakeSocialMatrix.append([33, 27, 40, 0, 23])
    fakeSocialMatrix.append([223, 12, 345, 23, 0])

    #start.normalizeSocialData(fakeSocialMatrix)
    start.startProcessing()

#########################################################
# End Partial Testing Block Entry
#########################################################

#########################################################
# Full Testing Block Entry
#########################################################

#Get the Json String Passed in from the Node and load it
jsonString = sys.argv[1]
sys.stdout.write(jsonString)
jsonObject = json.loads(jsonString)

#items from the json String
meeting_id = jsonObject['meeting_id'] #meeting id string
section_id = jsonObject['section_id'] #section id string
#meeting_id = '5a1f72593696231140b0e180'
#section_id = '5a1f72583696231140b0e111'

#for testing do sys.argv[1] if running test from iphone and node
#hard code jsonString if running python only test

f = open('log.txt', "w+")
f.write('test')

#sys.stdout.write(meeting_id)
#sys.stdout.write(section_id)

#print(meeting_id)
#print(section_id)

#print("Test For Meeting Picture " + str(testpicnum) + ":")
#create a new folder for the meeting with needed subfolders
current_directory = "C:"
meeting_directory = os.path.join(current_directory, str(meeting_id))
if not os.path.exists(meeting_directory):
    os.makedirs(meeting_directory)

crops_directory = os.path.join(meeting_directory, "crops")
if not os.path.exists(crops_directory):
    os.makedirs(crops_directory)

portraits_directory = os.path.join(meeting_directory, "portraits")
if not os.path.exists(portraits_directory):
    os.makedirs(portraits_directory)

portraits_cropped_directory = os.path.join(meeting_directory, "portraits_cropped")
if not os.path.exists(portraits_cropped_directory):
    os.makedirs(portraits_cropped_directory)

f.write('created directories')

#Create a new DataBase object and connect to the database
database = DataBase(meeting_id, section_id)
db = database.connectToDB()

f.write('connected to db')

#create the meeting object for the current meeting
meeting = database.getMeetingObject(db, meeting_directory, crops_directory, portraits_directory, portraits_cropped_directory)
sys.stdout.write("got meeting")


#get an array of Student objects for the current meeting
arrayStudents, classNumToStudentIdDict , studentIdToClassNumDict = database.getStudents(db, portraits_cropped_directory)
sys.stdout.write("got students")


for student in arrayStudents:
    print(student.getClassNumber())

meeting.setClassNumToStudentIdDict(classNumToStudentIdDict)
meeting.setStudentIdToClassNumDict(studentIdToClassNumDict)
meeting.setCountTotalStudents(len(arrayStudents))

if(meeting.getFirstMeeting() == False):
    database.getSocialData(meeting)

#print(classNumToStudentIdDict)

sys.stdout.write("start processing")


#set the image resize size for the whole program
size = 100
process = StartProcessing(meeting, arrayStudents, size, database, db)
output = process.begin()

sys.stdout.write("success")

#########################################################
# End Full Testing Block Entry
#########################################################
