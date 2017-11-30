from Meeting import *
from Student import *
import cv2
import glob 
from Matcher import *
from ImageProcessing import *
from Output import *
from DataBase import *

class StartProcessing():
    
    def __init__(self, meetingObject, arrayStudentObjects, size, database, db):
       self.meeting = meetingObject
       self.arrayStudents = arrayStudentObjects
       self.size = size
       self.database = database
       self.db = db

    def begin(self):
        #print("Starting processing")
        imageProcessor = ImageProcessing(self.meeting, self.arrayStudents, self.size)
        confidenceMatrix = imageProcessor.processImageAndGetConfidenceMatrix()
        print("done confidence:")
        for i in range(len(confidenceMatrix)):
            print(confidenceMatrix[i])

        useDelete = True
        useSocial = False
        matcher = Matcher(self.meeting, self.arrayStudents)
        attendance = matcher.matchStudents(confidenceMatrix, useDelete, useSocial)
        output = Output(self.meeting, self.arrayStudents, self.meeting.getCroppedFaces(), attendance)
        imageOrginalWithAttedance, imageAttendancePath = output.createAndWriteAttendacePiture("Matching")
        
        
        #write the attedance picture to the db
        self.database.writeImageWithAttendance(self.db, imageOrginalWithAttedance, self.meeting.getMeetingDirectory(), imageAttendancePath)

        #write the attedance to the db
        self.database.writeAttendance(self.db, self.arrayStudents)

        #write the average social matrix to the db if its
        if(self.meeting.getFirstMeeting() == True):
            finalAverageSocialMatrix = output.findSocialMatrixFirstMeeting()
        else:
            finalAverageSocialMatrix = output.findAverageSocialMatrix()
        
        self.database.writeSocialMatrix(self.db, self.meeting, finalAverageSocialMatrix, self.arrayStudents)

        output.printAttendance()
        if(1==2):
            useDelete = False
            useSocial = True
            matcher = Matcher(self.meeting, self.arrayStudents)
            attendance = matcher.matchStudents(confidenceMatrix, useDelete, useSocial)
            output4 = Output(self.meeting, self.arrayStudents, self.meeting.getCroppedFaces(), attendance)
            output4.createAndWriteAttendacePiture("SocialNoDelete")
            output4.printAttendance()

            useDelete = True
            useSocial = False
            matcher = Matcher(self.meeting, self.arrayStudents)
            attendance = matcher.matchStudents(confidenceMatrix, useDelete, useSocial)
            output3 = Output(self.meeting, self.arrayStudents, self.meeting.getCroppedFaces(), attendance)
            output3.createAndWriteAttendacePiture("Social")
            output3.printAttendance()

            useDelete = False
            useSocial = False
            matcher = Matcher(self.meeting, self.arrayStudents)
            attendance = matcher.matchStudents(confidenceMatrix, useDelete, useSocial)
            output2 = Output(self.meeting, self.arrayStudents, self.meeting.getCroppedFaces(), attendance)
            output2.createAndWriteAttendacePiture("MatchingNoDelete")
            output2.printAttendance()

        
        








    





