#GitHub Code

#############################################################################################################################
# Authors: Brandon Royal, Stephen Ulmer, Vien Yeung         
# 
# Description: Many to Many Matching for Facial Recognition using Social Circles as a Metric
# 
# Change Log:
#   - Brandon Royal - Initial
#   - Brandon Royal - Matching Algorithm
#   - Brandon Royal - Social Data Algorithm
#
#############################################################################################################################

import json
import numpy
import cv2
import sys
import math
from copy import deepcopy
from Output import *


##########################################
#GLOBAL VARIABLES FOR DUMMY VALUE TESTING
##########################################
fakeconfidenceMatrix = [] 
fakeconfidenceMatrix.append([12, 67, 70, 30, 100])
fakeconfidenceMatrix.append([70, 45, 48, 50, 55])
fakeconfidenceMatrix.append([85, 40, 45, 49, 50])
fakeconfidenceMatrix.append([60, 80, 49, 20, 70])
fakeconfidenceMatrix.append([45, 90, 80, 115, 18])

fakeSocialMatrix = []
fakeSocialMatrix.append([0, 3, 1, 1, 2, 3, 2, 2, 3, 2])
fakeSocialMatrix.append([3, 0, 3, 3, 2, 1, 2, 2, 1, 2])
fakeSocialMatrix.append([1, 3, 0, 1, 2, 3, 2, 2, 3, 2])
fakeSocialMatrix.append([1, 3, 1, 0, 2, 3, 2, 2, 3, 2])
fakeSocialMatrix.append([2, 2, 2, 2, 0, 2, 2, 2, 2, 2])
fakeSocialMatrix.append([3, 1, 3, 3, 2, 0, 2, 2, 1, 2])
fakeSocialMatrix.append([2, 2, 2, 2, 2, 2, 0, 2, 2, 2])
fakeSocialMatrix.append([2, 2, 2, 2, 2, 2, 2, 0, 2, 2])
fakeSocialMatrix.append([3, 1, 3, 3, 2, 1, 2, 2, 0, 2])
fakeSocialMatrix.append([2, 2, 2, 2, 2, 2, 2, 2, 2, 0])

arrayStudentIds = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]



class Matcher():

    def __init__(self, meetingObject, arrayStudentObjects):
       self.meeting = meetingObject
       self.students = arrayStudentObjects

    def genderRecognition(self, pictures):
        print('TODO')

    ##############################################################
    #FUNCTION: testMatching
    #test function to use dummy values with the confidence matrix
    #Time Complexity:
    #Space Complexity:
    ##############################################################
    def testMatching(self):
        #fake confidence Matrix
        #confidenceMatrix = mockMain()

        confidenceMatrix = mainStart()

        #print(fakeconfidenceMatrix)

        attendence = self.matchStudents(confidenceMatrix)

        #print('attendence')
        #print(attendence)

        dictionary = dict(zip(arrayStudentIds, attendence))

        json_string = json.dumps(dictionary)

        print(json_string)
    
    ##############################################################
    #FUNCTION startRecogniton
    #Main entry point for the matching. This function will be called to start the process of detection, recognition, and matching.
    #Time Complexity:
    #Space Complexity:
    ##############################################################
    def startRecognition(self):


        arrayStudentIds = self.student_ids
        meeting_id = self.meeting_id
        pathMeetingPic = self.pathMeetingPic
        arrayOfStudentPicPaths = self.arrayOfStudentPicPaths
        directory = self.directory

        confidenceMatrix = mainStart(arrayStudentIds, pathMeetingPic, arrayOfStudentPicPaths, directory)

        attendance = matchStudents(confidenceMatrix)

        dictionary = dict(zip(arrayStudentIds, attendance)) #{Student_id : attendance (0 or 1)}

        json_string = json.dumps(dictionary)

        return json_string

    ##############################################################
    #FUNCTION: decodeImage
    #Decodes a single image and returns the decoded image
    #Time Complexity:
    #Space Complexity:
    ##############################################################
    def decodeImage(image):
        decodedImage = imdecode(image)
        return decodedImage

    ##############################################################
    #FUNCTION: decodeArrayOfImages
    #Decodes a list of images and returns a new list with the decoded images 
    #Time Complexity:
    #Space Complexity:
    ##############################################################
    def decodeArrayOfImages(images):
        arrayImages = null
        index = 0
        for key in images:
            arrayImages[index] = (imdecode(image[key]))
            index = index + 1
        return arrayImages

    ##############################################################
    #FUNCTION: getStudentIDs
    #Gets each student id that is the key for the student picture in the passed in dictionary
    #Time Complexity:
    #Space Complexity:
    ##############################################################
    def getStudentIDs(Ids):
        arrayStudentIds = null
        index = 0
        for key in Ids:
            arrayStudentIds[index] = key
            index = index + 1

        return arrayStudentIds

    ##############################################################
    #FUNCTION: getConfidenceValues
    #Passes the class image and the student images to the Facial Detection and Recoginition Method and gets back a 2d Matrix of Confidence Values
    #Time Complexity:
    #Space Complexity:
    ##############################################################
    def getConfidenceValues(self, classImage, studentImages):
        confidenceMatrix = mainStart()
        return confidenceMatrix

    ##############################################################
    #FUNCTION: useSocial
    #Social function to determine matching. Used when two input faces have the same top match and their confidence values are within x% of eachother
    #Time Complexity:
    #Space Complexity:
    #
    #Parameters:
    #   dbSocialMatrix - 2d matrix with stored social values of (1-3) to show social 'closeness' to eachother. Student with self is 0, 1 is better 3 is worse
    #   inputSocialMatrix - 2d matrix with social 'closeness' of input faces based off distances in class picture. Still 1-3 and 0 meaning self
    #   inputFaceOne - first inputFace we are considering
    #   inputFaceTwo - second inputFace we are considering
    #   inputFaceOneConfidence - first inputFace confidence to the dbface
    #   inputFaceTwoConfidence - second inputFace confidence to the dbface
    #   dbFace is the top match that the two input faces have in common
    #   confirmedMatches - array of confirmed matches. each index i is an input face reference and each value of confirmedMatches[i] is the id of a student
    #   arrayStudnetIds - maps the index for each student dbFace to its studentId
    #############################################################
    def useSocial(self, dbSocialMatrix, inputSocialMatrix, inputFaceOne, inputFaceTwo, inputFaceOneConfidence, 
                  inputFaceTwoConfidence, dbFace, confirmedMatches):
        
        #First find who the db face is usually near by finding its 1 and 2 values
        socialValueOne = []
        socialValueTwo = []

        lengthDBSocialMatrix = len(dbSocialMatrix)
        numOnes = 0
        numTwos = 0

        for i in range(lengthDBSocialMatrix):
            if(dbSocialMatrix[dbFace][i] >= 1 and dbSocialMatrix[dbFace][i] < 1.5):
                socialValueOne.append(i)
                #print("Student " + str(dbFace) + " has a 1 connection to Student " + str(i))
                numOnes += 1
            if(dbSocialMatrix[dbFace][i] >= 1.5 and dbSocialMatrix[dbFace][i] < 2):
                socialValueTwo.append(i)
                #print("Student " + str(dbFace) + " has a 2 connection to Student " + str(i))
                numTwos += 1

        #Next we check who is near each input face one at a time. If they are matched, then check if the near person is near the dbFace usually
        
        lengthInputSocialMatrix = len(inputSocialMatrix)

        socialOneInputOne = []
        socialTwoInputOne = []
        numOnesInputOne = 0
        numTwosInputOne = 0

        socialOneInputTwo = []
        socialTwoInputTwo = []
        numOnesInputTwo = 0
        numTwosInputTwo = 0

        #find who is near for inputFaceOne
        for i in range(lengthInputSocialMatrix):
            if(inputSocialMatrix[inputFaceOne][i] == 1):
                socialOneInputOne.append(i)
                #print("Cropped Face " + str(inputFaceOne) + " has a 1 connection to Cropped Face " + str(i))
                numOnesInputOne += 1
            if(inputSocialMatrix[inputFaceOne][i] == 2):
                socialTwoInputOne.append(i)
                #print("Cropped Face " + str(inputFaceOne) + " has a 2 connection to Cropped Face " + str(i))
                numTwosInputOne += 1

        #find who is near for inputFaceTwo
        for i in range(lengthInputSocialMatrix):
            if(inputSocialMatrix[inputFaceTwo][i] == 1):
                socialOneInputTwo.append(i)
                #print("Cropped Face " + str(inputFaceTwo) + " has a 1 connection to Cropped Face " + str(i))
                numOnesInputTwo += 1
            if(inputSocialMatrix[inputFaceTwo][i] == 2):
                socialTwoInputTwo.append(i)
                #print("Cropped Face " + str(inputFaceTwo) + " has a 2 connection to Cropped Face " + str(i))
                numTwosInputTwo += 1

        #Now we search through who is near each input face to see if they have already been matched
        alreadyMatchedOneInputOne = []
        alreadyMatchedTwoInputOne = []
        numMatchedOneInputOne = 0
        numMatchedTwoInputOne = 0

        alreadyMatchedOneInputTwo = []
        alreadyMatchedTwoInputTwo = []
        numMatchedOneInputTwo = 0
        numMatchedTwoInputTwo = 0

        #For firt input face find the '1s' and '2s' that are already matched
        for i in range(numOnesInputOne):
            if(confirmedMatches[socialOneInputOne[i]] != -1):
                #print("for cropped face " + str(inputFaceOne) + " cropped face " + str(socialOneInputOne[i]) + " is a 1 and is already matched to student " + str(confirmedMatches[socialOneInputOne[i]]))
                alreadyMatchedOneInputOne.append(confirmedMatches[socialOneInputOne[i]]) #adds the student id to the already matched array
                numMatchedOneInputOne += 1
        for i in range(numTwosInputOne):
            if(confirmedMatches[socialTwoInputOne[i]] != -1):
                #print("for cropped face " + str(inputFaceOne) + " cropped face " + str(socialTwoInputOne[i]) + " is a 2 and is already matched to student " + str(confirmedMatches[socialTwoInputOne[i]]))
                alreadyMatchedTwoInputOne.append(confirmedMatches[socialTwoInputOne[i]]) #adds the student id to the already matched array
                numMatchedTwoInputOne += 1

        #For the second input face find the '1s' and '2s' that are already matched
        for i in range(numOnesInputTwo):
            if(confirmedMatches[socialOneInputTwo[i]] != -1):
                #print("for cropped face " + str(inputFaceTwo) + " cropped face " + str(socialOneInputTwo[i]) + " is a 1 and is already matched to student " + str(confirmedMatches[socialOneInputTwo[i]]))
                alreadyMatchedOneInputTwo.append(confirmedMatches[socialOneInputTwo[i]]) #adds the student id to the already matched array
                numMatchedOneInputTwo += 1
        for i in range(numTwosInputTwo):
            if(confirmedMatches[socialTwoInputTwo[i]] != -1):
                #print("for cropped face " + str(inputFaceTwo) + " cropped face " + str(socialTwoInputTwo[i]) + " is a 1 and is already matched to student " + str(confirmedMatches[socialTwoInputTwo[i]]))
                alreadyMatchedTwoInputTwo.append(confirmedMatches[socialTwoInputTwo[i]]) #adds the student id to the already matched array
                numMatchedTwoInputTwo += 1

        #Next we use the close ones matched and check if they are close with the database face
        #whichever out of input one and two have more '1s' and '2s' is who is accepted as a match for the dbFace
        #NOTE: at this point we are assuming that the dbSocialMatrix's indexes refer to a student id
        #   this will work if the student ids are 0 to N-1 for each class where N is the total number of students
        #   IF this does not work we can have an array that references 0 to N-1 to a student id

        countOnesInputOne = 0
        countTwosInputOne = 0

        countOnesInputTwo = 0
        countTwosInputTwo = 0

        #first input face
        for i in range(numMatchedOneInputOne):
            if(dbSocialMatrix[dbFace][alreadyMatchedOneInputOne[i]] >= 1 and dbSocialMatrix[dbFace][alreadyMatchedOneInputOne[i]] < 1.5):
                countOnesInputOne += 1        
                #print("for first cropped face, " + str(alreadyMatchedOneInputOne[i]) + " is already matched and is a 1 to the Student")
        #print("For first cropped face found " + str(countOnesInputOne) + " 1s")
        
        for i in range(numMatchedTwoInputOne):
            if(dbSocialMatrix[dbFace][alreadyMatchedTwoInputOne[i]] >= 1.5 and dbSocialMatrix[dbFace][alreadyMatchedTwoInputOne[i]] <= 2):
                countTwosInputOne += 1
                #print("for first cropped face, " + str(alreadyMatchedTwoInputOne[i]) + " is already matched and is a 2 to the Student")
        #print("For first cropped face found " + str(countTwosInputOne) + " 2s")


        #second input face
        for i in range(numMatchedOneInputTwo):
            if(dbSocialMatrix[dbFace][alreadyMatchedOneInputTwo[i]] >= 1 and dbSocialMatrix[dbFace][alreadyMatchedOneInputTwo[i]] < 1.5):
                countOnesInputTwo += 1
                #print("for second cropped face, " + str(alreadyMatchedOneInputTwo[i]) + " is already matched and is a 1 to the Student")
        #print("For second cropped face found " + str(countOnesInputTwo) + " 1s")

        for i in range(numMatchedTwoInputTwo):
            if(dbSocialMatrix[dbFace][alreadyMatchedTwoInputTwo[i]] >= 1.5 and dbSocialMatrix[dbFace][alreadyMatchedTwoInputTwo[i]] <= 2):
                countTwosInputTwo += 1
                #print("for second cropped face, " + str(alreadyMatchedTwoInputTwo[i]) + " is already matched and is a 2 to the Student")
        #print("For second cropped face found " + str(countTwosInputTwo) + " 2s")

        #now we know who is near both the input faces and the db face. This means for a given student, if they are a '1' compared
        #   to both the input face and the db face then we added to the count ones and if they are a '2' we did the same
        #   so for each input face we have two counts, the number of '1s' (the closest students) and the '2s' (the mildly close students).
        #   At this point we could simply say whoever has more '1s' accept as a match but because there could be many students not already matched
        #   which would affect this count, we instead are going to weigh the numbers where a '1' is worth more than a 2.
        #   This can be done by multiplying the number of '1s' by .x and number of twos by .x where x is higher for 1s than 2s.
        #   This in no way is a perfect algorithm but is an initial idea. Another idea would be to consider the '3s' also and say that if the student
        #   is not already matched they are assummed to be a 2 and then multiple the 1s, 2s, and 3s by .x, .y, and .z
        #   This again is not a perfectly robust idea and could fail in many circumstances such as if an input face '1s' are not matched but 3's are
        #   and then the '1s' become '2s'. There is a lot to consider in this section of the algorithm and tests will be done to determine which
        #   method is the most successful.

        #NOTE FOR NOW JUST CHECKING WHO HAS MORE ONES, THEN TWOS, THEN HIGHER CONFIDENCE
        if(countOnesInputOne > countOnesInputTwo):
            return 1
        if(countOnesInputOne < countOnesInputTwo):
            return 2
        if(countTwosInputOne > countTwosInputTwo):
            return 1
        if(countTwosInputOne < countTwosInputTwo):
            return 2

        return 1 if(inputFaceOneConfidence < inputFaceTwoConfidence) else 2

    #############################################################
    #
    #FUNCTION: matchStudents
    #Given a 2d confidence matrix of size n (number of faces in class pic) by m (number of total students in the class) matches
    #   an input face to a database face and returns a boolean array stating who was present or not
    #Time Complexity:
    #Space Complexity:
    ##############################################################
    def matchStudents(self, confidenceMatrix, useDelete, useSocial):
        
        #correctMatchesInputOne = {19, }

        minConfidence = 200
        topMatchesTaken = 10
        if(useSocial == True):
            closenessThreshold = 10
        else:
            closenessThreshold = -1

        #if it is the first meeting we have no social data to use
        if(self.meeting.getFirstMeeting() == True):
            closenessThreshold = -1

        print()

        #this is number of faces retrieved from the class portrait picture
        numberCropped = len(confidenceMatrix)
        #print("Number of cropped faces: " + str(numberCropped))

        #this is the number of total students in the class
        numberTotalStudents = len(confidenceMatrix[0]) 
        #print("Total Number of Students in the class: " + str(numberTotalStudents))


        #2d matrix that stores the top k matches for each cropped face
        topMatches  = [[-1 for i in range(topMatchesTaken)] for j in range(numberCropped)]

        
        #print("Number of Cropped Faces: " + str(len(topMatches)))
        #print("Top Matches taken: " + str(len(topMatches[0])))
        
        #create a copy of the confidence matrix that we can edit the values of for finding the top k matches
        editableConfidenceMatrix = deepcopy(confidenceMatrix)

        #print('confidence', confidenceMatrix)

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
        #print('confidence', confidenceMatrix)
        #print(topMatches)

        #for i in range(len(confidenceMatrix)):
        #    print(confidenceMatrix[i])

        #for i in range(numberCropped):
        #    print("Student #" +str(i)+"'s top matches are: ")
        #    print(topMatches[i])

        
        #array to track "final" matches, the index is the cropped face id, the value of each index is the corresponding student portrait match
        finalMatch = [-1 for i in range(numberCropped)]

        #dictionary where each student (identified by class num) is the key and the value is the students matched cropped face (-1) if no match
        matchDictionary = {}
        for i in range(numberTotalStudents):
            matchDictionary[i] = -1

        alreadyMatchedCropped = [False for i in range(numberCropped)]
        alreadyMatchedPortrait = [False for i in range(numberTotalStudents)]
        arrayMatchesLeft = [topMatchesTaken for i in range(numberCropped)]

        if(useDelete == True):
            for i in range(numberCropped):
                topMatch = topMatches[i][0]
                unique = True
                for j in range(numberCropped):
                    if(j != i):
                        curTopMatch = topMatches[j][0]
                        if(topMatch == curTopMatch):
                            unique = False
                if(unique == True):
                    alreadyMatchedCropped[i] = True
                    alreadyMatchedPortrait[topMatch] = True
                    finalMatch[i] = topMatch
                    matchDictionary[topMatch] = i
                    #set match for cropped face
                    self.meeting.getCroppedFaces()[i].setStudentMatchClassNum(topMatch)
                    self.meeting.getCroppedFaces()[i].setStudentMatchId(self.meeting.getClassNumToStudentIdDict()[topMatch])
                    self.meeting.getCroppedFaces()[i].setRecognized(True)
                    fullname = self.students[topMatch].getFullName()
                    self.meeting.getCroppedFaces()[i].setStudentMatchFullName(fullname)
                    #set match for student
                    #NEED TO SET MATCHED SOCIAL ARRAY, THIS WAY ALL MATCHED STUDENTS WILL HAVE A MATCHED SOCIAL ARRAY BUT IF A STUDENT IS ABSENT IT WILL BE 
                    #AN EMPTY ARRAY AND WE CAN THEN INSTEAD USE THE PREVIOUS AVERAGED SOCIAL DATA INPLACE TO NOT RUIN THE CURRENT SOCIAL AVERAGE
                    self.students[topMatch].setPresent(True)
                    self.students[topMatch].setCroppedFaceMatchId(i)
                    self.students[topMatch].setCroppedFaceMatchPath(self.meeting.getCroppedFaces()[i].getCroppedImagePath())
                    print("Cropped Face " + str(i) + " is found to be student " + str(topMatch))

        print("done with initial delete")

        allMatched = True
        for i in range(numberCropped):
            if(finalMatch[i] == -1):
                allMatched = False

        for i in range(numberCropped):
            if(alreadyMatchedCropped[i] == True or allMatched == True):
                    continue
            while(arrayMatchesLeft[i] > 0):
                
                allMatched = True
                for i in range(numberCropped):
                    if(finalMatch[i] == -1):
                        allMatched = False
                if(allMatched):
                    break

                #print('top matches', topMatches)
                topMatch = topMatches[i][0]
                #print("for cropped face " + str(i) + " we are considering student " + str(topMatch))
                if(alreadyMatchedPortrait[topMatch] == True):
                    del topMatches[i][0]
                    continue
                deleted = False
                for j in range(numberCropped):
                    if(j != i and arrayMatchesLeft[j] > 0):
                        curTopMatch = topMatches[j][0]
                        #print(topMatch, " ", curTopMatch)
                        if(topMatch == curTopMatch):
                            if(abs(confidenceMatrix[i][topMatch] - confidenceMatrix[j][curTopMatch]) <= closenessThreshold):
                               print('Use Social for cropped face ' + str(i) + " vs cropped face " + str(j) + " to match to student " + str(topMatch))
                               socialResult = self.useSocial(self.meeting.getAverageSocialMatrix(), self.meeting.getUnrecognizedSocialMatrix(), i , j, confidenceMatrix[i][topMatch], confidenceMatrix[j][curTopMatch], topMatch, finalMatch)
                               if(socialResult == 1):
                                   print("using social choose: " + str(i))
                                   del topMatches[j][0]
                                   arrayMatchesLeft[j] = arrayMatchesLeft[j] - 1
                               elif(socialResult == 2):
                                    print("using social choose: " + str(j))
                                    del topMatches[i][0]
                                    arrayMatchesLeft[i] = arrayMatchesLeft[i] - 1
                                    deleted = True
                                    break
                            else:
                                if(confidenceMatrix[i][topMatch] < confidenceMatrix[j][curTopMatch]):
                                    del topMatches[j][0]
                                    arrayMatchesLeft[j] = arrayMatchesLeft[j] - 1
                                    #print('remove this student as a top match for the right list')
                                elif(confidenceMatrix[i][topMatch] > confidenceMatrix[j][curTopMatch]):
                                    del topMatches[i][0]
                                    deleted = True
                                    arrayMatchesLeft[i] = arrayMatchesLeft[i] - 1
                                    #print('remove this student as a top match for the left list')
                                    break
                                    
                if deleted == False:
                    finalMatch[i] = topMatch
                    matchDictionary[topMatch] = i
                    alreadyMatchedCropped[i] = True
                    alreadyMatchedPortrait[topMatch] = True
                    #set match for cropped face
                    self.meeting.getCroppedFaces()[i].setStudentMatchClassNum(topMatch)
                    self.meeting.getCroppedFaces()[i].setStudentMatchId(self.meeting.getClassNumToStudentIdDict()[topMatch])
                    self.meeting.getCroppedFaces()[i].setRecognized(True)
                    fullname = self.students[topMatch].getFullName()
                    self.meeting.getCroppedFaces()[i].setStudentMatchFullName(fullname)
                    #set match for student
                    #NEED TO SET MATCHED SOCIAL ARRAY, THIS WAY ALL MATCHED STUDENTS WILL HAVE A MATCHED SOCIAL ARRAY BUT IF A STUDENT IS ABSENT IT WILL BE 
                    #AN EMPTY ARRAY AND WE CAN THEN INSTEAD USE THE PREVIOUS AVERAGED SOCIAL DATA INPLACE TO NOT RUIN THE CURRENT SOCIAL AVERAGE
                    self.students[topMatch].setPresent(True)
                    self.students[topMatch].setCroppedFaceMatchId(i)
                    self.students[topMatch].setCroppedFaceMatchPath(self.meeting.getCroppedFaces()[i].getCroppedImagePath())
                    print("Cropped Face " + str(i) + " is found to be student " + str(topMatch))
                    break
        self.meeting.setMatchDictionary(matchDictionary)
        self.meeting.setFinalMatches(finalMatch)
        return finalMatch







