from PIL import Image
import cv2
from CroppedFace import *
import numpy
import math
from Meeting import *
from Student import *
import json
import sys
from copy import deepcopy

class Output():
    
    def __init__(self, meeting, arrayStudents, arrayCroppedFaces, attendance):
        self.meeting = meeting
        self.students = arrayStudents
        self.croppedFaces = arrayCroppedFaces
        self.attendance = attendance

    def createAndWriteAttendacePiture(self, appendToName):
        imageOrginal = cv2.imread(self.meeting.getMeetingPicPath())
        imageOrginalWithAttedance = imageOrginal.copy()

        for cropped in self.croppedFaces:
            x, y, w, h = cropped.getOrginalCoordinates()
            imageOrginalWithAttedance = cv2.rectangle(imageOrginalWithAttedance, (x, y), (x+w, y+h), (0, 255, 0), 5)
            fullname = cropped.getStudentMatchFullName()
            if(fullname == ""):
                fullname = "Does Not Belong"
            imageOrginalWithAttedance = cv2.putText(imageOrginalWithAttedance, fullname, (x,y-10), cv2.FONT_HERSHEY_COMPLEX, 1.1, (0, 255, 255), 3)
        path = self.meeting.getMeetingDirectory() + "//attendace_results" + appendToName + ".jpg"
        cv2.imwrite(path, imageOrginalWithAttedance)
        return imageOrginalWithAttedance, path

    def printAttendance(self):
        for student in self.students:
            if(student.getPresent() == True):
                print(student.getFullName() + ": Present")
            else:
                print(student.getFullName() + ": Absent")

    def findAverageSocialMatrix(self):
        dbMatrix = self.meeting.getAverageSocialMatrix()
        croppedMatrix = self.meeting.getUnrecognizedSocialMatrix()
        scaledCroppedMatrix = [[0 for i in range(len(dbMatrix))] for j in range(len(dbMatrix))]
        finalAverageMatrix = [[-1 for i in range(len(dbMatrix))] for j in range(len(dbMatrix))]
        
        #first for any absent students place the value from the db matrix into the new matrix
        for student in self.students:
            if (student.getCroppedFaceMatchId() == -1):
                for i in range(len(scaledCroppedMatrix)):
                    scaledCroppedMatrix[student.getClassNumber()][i] = dbMatrix[student.getClassNumber()][i]
                    scaledCroppedMatrix[i][student.getClassNumber()] = dbMatrix[i][student.getClassNumber()]

        matchDictionary = self.meeting.getMatchDictionary() 
        #now using the match dictionary reoganize the croppedMatrix to have the right indexing for the dbMatrix
        for i in range(len(dbMatrix)):
            if(self.students[i].getCroppedFaceMatchId() != -1):
                for j in range(len(dbMatrix)):
                    if(self.students[i].getCroppedFaceMatchId() != -1):
                        scaledCroppedMatrix[i][j] = croppedMatrix[matchDictionary[i]][matchDictionary[j]]

        
        #now we find the average by doing ((DB * numMeetings) + cropped)/numMeetings+1
        for i in range(len(dbMatrix)):
            for j in range(len(dbMatrix)):
                finalAverageMatrix[i][j] = (((dbMatrix[i][j] * self.meeting.getCountMeetings()) + scaledCroppedMatrix[i][j]) / (self.meeting.getCountMeetings() + 1))

        return finalAverageMatrix

    def findSocialMatrixFirstMeeting(self):
        
        matchDictionary = self.meeting.getMatchDictionary()
        croppedMatrix = self.meeting.getUnrecognizedSocialMatrix()
        scaledCroppedMatrix = [[0 for i in range(len(matchDictionary))] for j in range(len(matchDictionary))]
        
        finalMatches = self.meeting.getFinalMatches()
        for i in range(len(croppedMatrix)):
            if(finalMatches[i] == -1):
                continue
                for j in range(len(croppedMatrix)):
                        scaledCroppedMatrix[i][j] = croppedMatrix[matchDictionary[i]][matchDictionary[j]]
        return scaledCroppedMatrix





            

