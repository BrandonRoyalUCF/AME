#############################################################################################################################
# Authors: Brandon Royal, Stephen Ulmer, Vien Yeung         
# 
# Description: Using the orginal image and the depth data image, determines the social relationship between individuals
# 
# Change Log:
#   - Brandon Royal - Initial
#
#############################################################################################################################

from PIL import Image
import cv2
from CroppedFace import *
import numpy
import math

class DepthProcessing():
    
    def __init__(self, meeting, arrayStudents, size):
        self.meeting = meeting
        self.arrayStudents = arrayStudents
        self.size = size

    def beginDepthProcessing(self):

        cascPath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascPath)

        ##open the images using Pil (use this if the shape idea does not work)
        #orginalImage = Image.open(self.meeting.getMeetingPicPath())
        #depthImage = Image.open(self.meeting.getDepthPicPath())
        ##get each images dimensions 
        #orginalWidth, orginalHeight = orginalImage.size
        #depthHeight, depthWidth = depthImage.size

        #read images into open cv and detect the faces
        imageOrginal = cv2.imread(self.meeting.getMeetingPicPath())
        imageDepth = cv2.imread(self.meeting.getDepthPicPath(), 0)

        originalWidth, originalHeight = imageOrginal.shape[:2]
        depthWidth, depthHeight  = imageDepth.shape[:2]

        #print(originalWidth, originalHeight)
        #print(depthWidth, depthHeight)

        #determine the scaling multiplier based of the ratio of the depth to orginal width and height
        coordinateXMultiplier = depthWidth/originalWidth
        coordinateYMultiplier = depthHeight/originalHeight

        #gray = cv2.cvtColor(imageDepth, cv2.COLOR_BGR2GRAY)

        #img = cv2.imread(self.depthImagePath, 0) #since the image is grayscale, we need only one channel and the value '0' indicates just that
        #for i in range (img.shape[0]): #traverses through height of the image
        #    for j in range (img.shape[1]): #traverses through width of the image
        #        print(img[i][j])

        imageDepthWithDetection = imageDepth.copy()
        imageOrginalWithDetection = imageOrginal.copy()

        imageOrginal = cv2.cvtColor(imageOrginal, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(imageOrginal, scaleFactor=1.2, minNeighbors=10, minSize=(30, 30))
        id = 0
        #print(imageDepth)
        #print(numpy.mean(imageDepth))
        croppedList = []
        for (x, y, w, h) in faces:

            #first lets crop the faces from the meeting pic and save them for later use
            cropImg = imageOrginal[y:y+h, x:x+w]
            #gray = cv2.cvtColor(cropImg, cv2.COLOR_BGR2GRAY)  # turn portrait to grayscale
            shrink = cv2.resize(cropImg, (self.size, self.size))
            cropImgPath = self.meeting.getCropsDirectory()+"//"+str(id)+'.jpg'
            cv2.imwrite(cropImgPath, shrink)
            #print("wrote cropped face " + str(id))

            #next we get the face coordinates for the depth image based off the multiplier found earlier
            xs = int(x*coordinateXMultiplier)
            xws = int((x+w)*coordinateXMultiplier)
            ys = int(y*coordinateYMultiplier)
            yhs = int((y+h)*coordinateYMultiplier)
            #print("Depth Face Bounds")
            #print(xs, xws, ys, yhs)
            

            #save a copy of the meeting pic with detection info
            imageOrginalWithDetection = cv2.rectangle(imageOrginalWithDetection, (x, y), (x+w, y+h), (0, 255, 0), 5)
            imageOrginalWithDetection = cv2.putText(imageOrginalWithDetection, 'F' + str(id), (x,y), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 255, 255), 5)
            
            count = 0
            total = 0
            #print("i:")
            #print(len(imageDepth))
            #print(xs, xws)
            #print()
            #print("j:")
            #print(len(imageDepth[0]))
            #print(ys, yhs)
            for i in range (xs, xws): #traverses through height of the image
                for j in range (ys, yhs): #traverses through width of the image
                    count = count + 1
                    total = total + imageDepth[j][i]
                    #print(count, gray[i][j])
            averageGreyScale = total/count
            distanceCameraToStudent = 1/(averageGreyScale/255)

            distanceFeet = 3.28084 * distanceCameraToStudent * 2
            distanceInches = distanceFeet * 12
            #print(total, count, averageGreyScale, distanceCameraToStudent, distanceFeet, distanceInches)

            #save a copy of the depth pic with detection info
            
            imageDepthWithDetection = cv2.rectangle(imageDepthWithDetection, (int(x*coordinateXMultiplier), int(y*coordinateYMultiplier)), (int((x+w)*coordinateXMultiplier), int((y+h)*coordinateYMultiplier)), (0, 255, 0), 2)
            imageDepthWithDetection = cv2.putText(imageDepthWithDetection, 'F' + str(id), (int(x*coordinateXMultiplier),int(y*coordinateYMultiplier)), cv2.FONT_HERSHEY_COMPLEX, .3, (0, 255, 255), 1)
            
            faceMidPointDepth = int((xs+(xws/2))), int((ys+(yhs/2)))

            faceMidPointOriginal = int(x+(w/2)), int(y+(h/2))

            xm = int((xs+(xws/2)))
            ym = int((ys+(yhs/2)))

            #print("Midpoint: " + str(faceMidPoint))
            
            #path = str(id) + ".jpg"
            croppedFace = CroppedFace(id, x, y, w, h, int(x*coordinateXMultiplier), int(y*coordinateYMultiplier), int((x+w)*coordinateXMultiplier), int((y+h)*coordinateYMultiplier), cropImgPath, averageGreyScale, faceMidPointOriginal, distanceCameraToStudent)
            croppedList.append(croppedFace)
            id = id + 1
        
        #cv2.imwrite("orginalDetection.jpg", imageOrginal)
        #cv2.imwrite("depthDetection.jpg", imageDepth)
        cv2.imwrite(self.meeting.getMeetingDirectory() + "//" + "meetingPicWithDetection.jpg", imageOrginalWithDetection)
        cv2.imwrite(self.meeting.getMeetingDirectory() + "//" + "depthPicWithDetection.jpg", imageDepthWithDetection)
        #print("wrote meeting pic and depth pic with detection")

        self.meeting.setCroppedFaces(croppedList)
        finalDistanceMatrix = self.createDistanceMatrix(croppedList)
        normalizedDistanceMatrix = self.normalizeSocialData(finalDistanceMatrix)
        self.meeting.setUnrecognizedSocialMatrix(normalizedDistanceMatrix)

    def createDistanceMatrix(self, croppedList):

        degreesPerPixel = .0108

        numStudents = len(croppedList)
        distanceMatrix = [[0 for x in range(numStudents)] for y in range(numStudents)]
        for face in croppedList:
            for otherFace in croppedList:
                if(face.getId() == otherFace.getId()):
                    continue
                pixelsBetween = self.pixelsBetweenFaces(face.getMidPoint()[0], face.getMidPoint()[1], otherFace.getMidPoint()[0], otherFace.getMidPoint()[1])
                theta = pixelsBetween * degreesPerPixel
                finalDistanceBetween = self.getActualDistanceBetweenFaces(face.getDistanceFromCamera(), otherFace.getDistanceFromCamera(), theta)
                distanceMatrix[face.getId()][otherFace.getId()] = finalDistanceBetween
                #print(pixelsBetween, theta)
                #print("Distance Between " + str(face.getId()) + " and " + str(otherFace.getId()) + " is " + str(finalDistanceBetween))
                #print()
            

        return distanceMatrix

    def pixelsBetweenFaces(self, x1, y1, x2, y2):
        a = abs(x2-x1)
        b = abs(y2-y1)
        c = math.sqrt((a*a) + (b*b))
        return c

    def getActualDistanceBetweenFaces(self, a, b, theta):
        radians = theta * 0.0174533
        return math.sqrt((a*a)+(b*b)-(2*a*b*math.cos(radians)))


    def normalizeSocialData(self, distanceMatrix):
        numStudents = len(distanceMatrix)
        allDistances = []

        #put all distances inside a one dimensional array
        for i in range(numStudents):
            for j in range(numStudents):
                if(distanceMatrix[i][j] != 0):
                    allDistances.append(distanceMatrix[i][j])

        #sort the array 
        allDistances.sort()

        #find the three partitions of the array
        first = 0
        second = int(((numStudents*numStudents) - numStudents)/3)
        third = (second*2)

        firstMin = 0
        firstMax = allDistances[second-1]
        secondMin = allDistances[second]
        secondMax = allDistances[third-1]
        thirdMin = allDistances[third]

        #print(allDistances)

        normalizedMatrix = [[0 for x in range(numStudents)] for y in range(numStudents)]

        for i in range(numStudents):
            for j in range(numStudents):
                value = distanceMatrix[i][j]
                if(value <= firstMax and value > 0):
                    normalizedMatrix[i][j] = 1
                elif(value >= secondMin and value <= secondMax):
                    normalizedMatrix[i][j] = 2
                elif(value >= thirdMin):
                    normalizedMatrix[i][j] = 3
        #print()

        #for i in range(numStudents):
        #    print(distanceMatrix[i])

        #print()
        #for i in range(numStudents):
        #    print(normalizedMatrix[i])

        return normalizedMatrix









        

        




