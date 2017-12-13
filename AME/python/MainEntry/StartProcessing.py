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
        confidenceMatrix, baseAttendaceDict = imageProcessor.processImageAndGetConfidenceMatrix()
        print("done confidence:")
        for i in range(len(confidenceMatrix)):
            print(confidenceMatrix[i])

        useDelete = True
        useSocial = True
        matcher = Matcher(self.meeting, self.arrayStudents)

        #attendance with social data
        attendance = matcher.matchStudents(confidenceMatrix, False, useSocial)
        f = open(self.meeting.getMeetingDirectory() + '\AttendanceSocial.txt', "w+")
        count = 0
        for item in attendance:
            f.write('student: ' + str(item) + ' is found to be cropped face: ' + str(count) + '\n')
            count = count + 1

        #attendance to log without social data
        attendanceNoSocial = matcher.matchStudents(confidenceMatrix, useDelete, False)
        f = open(self.meeting.getMeetingDirectory() + '\AttendanceNoSocial.txt', "w+")
        count = 0
        for item in attendanceNoSocial:
            f.write('student: ' + str(item) + ' is found to be cropped face: ' + str(count) + '\n')
            count = count + 1

        output = Output(self.meeting, self.arrayStudents, self.meeting.getCroppedFaces(), attendance)
        imageOrginalWithAttedance, imageAttendancePath = output.createAndWriteAttendacePiture("MatchingWithSocial")

        #create attendace picture for social not used
        output.createAndWriteAttendancePictureTwo("MatchingNoSocial", attendanceNoSocial)

        #create attendance picture for base recognition
        output.createAndWriteAttendancePictureTwo("BaseRecognition", baseAttendaceDict)
        
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

        
        








    





