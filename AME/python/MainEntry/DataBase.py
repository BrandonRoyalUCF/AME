from Meeting import *
from Student import *
import cv2
from io import BytesIO
from pymongo import *
from bson.objectid import ObjectId
from gridfs import *
import numpy as np
import json


class DataBase():
    
    def __init__(self, meetingId, sectionId):
        self.meetingId = meetingId
        self.sectionId = sectionId

    def connectToDB(self):
        #client = MongoClient('mongodb://10.171.204.168:27017/')
        client = MongoClient('mongodb://localhost:27017/')
        db = client['test']
        return db

    def getMeetingObject(self, db, meeting_directory, crops_directory, portraits_directory, portraits_cropped_directory):
        sections = db['sections']
        currentSection = sections.find_one({"_id": ObjectId(self.sectionId)})
        meetings = currentSection['meetings']
        count = 0
        for meeting in meetings:
            count+=1
        firstMeeting = False
        if(count == 1):
            firstMeeting = True

        print(count, firstMeeting)


        meetings = db['meetings']
        currentMeeting = meetings.find_one({"_id": ObjectId(self.meetingId)})
        
        #get the meeting pic from the database and save it to the current folder
        meetingPicId = currentMeeting['meetingPicAttachment_id']
        attachments = GridFS(db, collection = 'attachments')  
        meetingPicStream = attachments.get(ObjectId(meetingPicId)).read()
        meetingPicNumpy = np.fromstring(meetingPicStream, np.uint8)
        meeting_img_np = cv2.imdecode(meetingPicNumpy, cv2.IMREAD_COLOR)
        meetingPicFinalPath = meeting_directory + "\\meeting_pic.jpg"
        cv2.imwrite(meetingPicFinalPath, meeting_img_np)

        #get the depth pic from the database and save it to the current folder
        depthPicId = currentMeeting['depthPicAttachment_id']
        depthPicStream = attachments.get(ObjectId(depthPicId)).read()
        depthPicNumpy = np.fromstring(depthPicStream, np.uint8)
        depth_img_np = cv2.imdecode(depthPicNumpy, cv2.IMREAD_COLOR)
        depthPicFinalPath = meeting_directory + "\\depth_pic.jpg"
        cv2.imwrite(depthPicFinalPath, depth_img_np)

        meeting = Meeting(self.meetingId, meetingPicFinalPath, depthPicFinalPath, meeting_directory, crops_directory, portraits_directory, portraits_cropped_directory, firstMeeting, count)
        #print("got meeting")
        return meeting

    def getStudents(self, db, portraits_cropped_directory):
        sections = db['sections']
        currentSection = sections.find_one({"_id": ObjectId(self.sectionId)})
        students = currentSection['students']
        arrayStudentIds = []
        for student in students:
            arrayStudentIds.append(student["_id"])

        arrayStudents = []
        num = 0
        allStudents = db['students']
        classNumToStudentIdDict = {}
        studentIdToClassNumDict = {}
        for id in arrayStudentIds:
            classNumber = num
            num += 1
            student = allStudents.find_one({"_id": ObjectId(id)})
            studentID = student['studentID']
            firstName = student['firstName']
            lastName = student['lastName']
            portraitIds = student['studentPortraitAttachment_ids']
            attachments  = db['Attachment']
            classNumToStudentIdDict[classNumber] = studentID
            studentIdToClassNumDict[studentID] = classNumber
            ascii = 97
            for id in portraitIds:
                hold = 0
                attachments = GridFS(db, collection = 'attachments')
                portraitStream = attachments.get(ObjectId(id)).read()
                portraitPicNumpy = np.fromstring(portraitStream, np.uint8)
                portrait_img_np = cv2.imdecode(portraitPicNumpy, cv2.IMREAD_COLOR)
                portraitDirectory = portraits_cropped_directory + '/' + str(classNumber) + '.' + chr(ascii) + ".jpg"
                ascii += 1
                cv2.imwrite(portraitDirectory, portrait_img_np)
                print("Wrote image " + str(classNumber) + '.' + chr(ascii) + ".jpg")
            socialData = None
            currentStudent = Student(studentID, classNumber, firstName, lastName, socialData)
            arrayStudents.append(currentStudent)
        #print("got all students")
        return arrayStudents, classNumToStudentIdDict, studentIdToClassNumDict

    def getSocialData(self, db, meeting):

        #determine how many students there are and setup an empty social matrix
        numberStudents = meeting.getCountTotalStudents()
        socialMatrix = [[0 for i in range(numberStudents)] for j in range(numberStudents)]

        #get the mapping of student ids to class number for the current students
        mappings = meeting.getStudentIdToClassNumDict()

        sections = db['sections']
        currentSection = sections.find_one({"_id": ObjectId(self.sectionId)})
        socialData = currentSection['socialData']
        for student in socialData:
            mainId = student['student_id']
            mainClassNum = mappings[mainID]
            for relation in socialData['relationships']:
                secondId = relation['student_id']
                secondClassNum = mappings[secondId]
                value = relation['value']
                socialMatrix[mainClassNum][secondClassNum] = value

        meeting.setAverageSocialMatrix(socialMatrix)

    def writeSocialMatrix(self, db, meeting, finalAverageSocialMatrix, students):
        sections = db['sections']
        currentSection = sections.find_one({"_id": ObjectId(self.sectionId)})
        socialData = currentSection['socialData']
        result = sections.update_one({"_id": ObjectId(self.sectionId)}, {"$set": {"socialData" : []}})


        for student in students:
            id = student.getId()
            classNum = student.getClassNumber()
            relations = []
            for student2 in students:
                otherId  = student2.getId()
                otherClassNum = student2.getClassNumber()
                value = finalAverageSocialMatrix[classNum][otherClassNum]
                relations.append({"student_id" : otherId, "value" : value})
            result = sections.update_one({"_id": ObjectId(self.sectionId)}, {"$push": {"socialData" : {"student_id" : id, "relationships" : relations}}})

        #meetings.update_one({"_id": ObjectId(self.meetingId)},{"$set": {"meetingPicAttachment_id": id}})

    def writeImageWithAttendance(self, db, image, meeting_directory, imagePath):
        #add the file to the database
        attachments = GridFS(db, collection = 'attachments')
        imagebytes = open(imagePath, "rb").read()
        id = attachments.put(imagebytes, filename = 'AttendanceImage.jpg')

        #add the new file id to the meeting
        meetings = db['meetings']
        meetings.update_one({"_id": ObjectId(self.meetingId)},{"$set": {"labeledMeetingPicAttachment_id": id}}) #NEEDS TO CHANGE TO RIGHT ID FOR MEETINGPICATTACHMENT_ID

        #TESTING ONLY TO SEE IF IMAGE CORRECTLY WRITTEN#
        #meetingPicStream = attachments.get(ObjectId(id)).read()
        #meetingPicNumpy = np.fromstring(meetingPicStream, np.uint8)
        #meeting_img_np = cv2.imdecode(meetingPicNumpy, cv2.IMREAD_COLOR)
        #meetingPicFinalPath = meeting_directory + "\\DataBaseAttendanceImage.jpg"
        #cv2.imwrite(meetingPicFinalPath, meeting_img_np)

    def writeAttendance(self, db, students):
        meetings = db['meetings'] 
        for student in students:
            id = student.getId()
            present = student.getPresent()
            result = meetings.update_one({"_id": ObjectId(self.meetingId)}, {"$push": {"attendance" : {"student_id" : id, "present" : present}}})
            print(result)



    





    



        


