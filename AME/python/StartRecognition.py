import json
import numpy
import cv2
import sys
import math

class StartRecognition():

    def __init__(self, jsonObject):
        self.json = jsonObject

    def startRecognition(self):
        jsonObject = json.loads(self.json)

        meetingPic = jsonObject['newMeeting']
        studentPics = jsonObject['studentPictures']

        decodedMeeting = decodeImage(meetingPic)
        decodedStudents = decodeArrayOfImages(studentPics)

        arrayStudentIds = getStudentIDs(studentPics)

        confidenceMatrix = getConfidenceValues(decodedMeeting, decodedStudents)

        attendence = matchStudents(confidenceMatrix)

        dictionary = dict(zip(arrayStudentIds, attendence))

        json_string = json.dumps(dictionary)

        return json_string

    def decodeImage(image):
        decodedImage = imdecode(image)
        return decodedImage

    def decodeArrayOfImages(images):
        arrayImages = null
        index = 0
        for key in images:
            arrayImages[index] = (imdecode(image[key]))
            index = index + 1
        return arrayImages

    def getStudentIDs(Ids):
        arrayStudentIds = null
        index = 0
        for key in Ids:
            arrayStudentIds[index] = key
            index = index + 1

        return arrayStudentIds

    def getConfidenceValues(classImage, studentImages):
        #confidenceMatrix = Confidence.getConfidence(classImage, studentImages)
        return confidenceMatrix

    def matchStudents(confidenceMatrix):
        
        minConfidence = 70
        topMatchesTaken = 3
        closenessThreshold = 7

        #this is number of faces retrieved from the class portrait picture
        numberCropped = len(confidenceMatrix)

        #this is the number of total students in the class
        numberTotalStudents = len(confidenceMatrix[0]) 

        

        #2d matrix that stores the top k matches for each cropped face
        topMatches  = [[-1 for i in range(numberCropped)] for j in range(topMatchesTaken)]
        
        #create a copy of the confidence matrix that we can edit the values of for finding the top k matches
        editableConfidenceMatrix = list(confidenceMatrix)

        #for each cropped face find the top j matches and put them into the topMatches array
        #topMatches[i] refers to each cropped face, topMatches[j] refers to the index of a student picture  
        for i in range(numberCropped):
            for j in range(topMatchesTaken):
                best = sys.maxsize
                bestIndex = -1
                for k in range(numberTotalStudents):
                    if(editableConfidenceMatrix[i][k] < best):
                        best = editableConfidenceMatrix[i][k]
                        bestIndex = k
                topMatches[i][j] = bestIndex
                editableConfidenceMatrix[i][bestIndex] = sys.maxsize
        
        #array to track "final" matches
        finalMatch = [-1 for i in range(numberCropped)]

        for i in range(numberCropped):
            while(topMatches[i][0] is not None):
                topMatch = topMatches[i][0]
                deleted = False
                for j in range(numberCropped):
                    if(j != i):
                        curTopMatch = topMatches[j][0]
                        if(topMatch == curTopMatch):
                            if(abs(confidenceMatrix[i][topMatch] - confidenceMatrix[j][curTopMatch]) <= closenessThreshold):
                               print('Use Social')
                            else:
                                if(confidenceMatrix[i][topMatch] < confidenceMatrix[j][curTopMatch]):
                                    del topMatches[j][0]
                                    print('remove this student as a top match for the right list')
                                elif(confidenceMatrix[i][topMatch] > confidenceMatrix[j][curTopMatch]):
                                    del topMatches[i][0]
                                    deleted = True
                                    break
                                    print('remove this student as a top match for the left list')
                    if deleted == False:
                        finalMatch[i] = topMatch








        

        maxMatch = null

        for i in range(numberCropped):
            maxMatch[i] = -1
            max = 50
            for j in range(numberTotalStudents):
                if max < confidenceMatrix[i][j]:
                    max = confidenceMatrix[i][j]
                    maxMatch[i] = j

        #for i in range(matrixSize):
        #    for j in range(i+1, matrixSize):
        #        if(maxMatch[i] == maxMatch[j]):
        #            print('here')
        #            #do logic

        isPresent = [False for i in range(matrixSize)]
        
        for i in range(matrixSize):
            if maxMatch[i] != -1:
                isPresent[i] = True


        return isPresent

print(cv2.__version__)
jsonObject = 'test'
start = StartRecognition(jsonObject)
finalJson = start.startRecognition()





