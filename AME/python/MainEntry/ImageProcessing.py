import cv2
import os
import numpy
import glob
from DepthProcessing import *

class ImageProcessing():
    
    def __init__(self, meetingObject, arrayStudentObjects, size):
        self.meeting = meetingObject
        self.arrayStudents = arrayStudentObjects
        self.cascPath = "haarcascade_frontalface_default.xml"
        self.faceCascade = cv2.CascadeClassifier(self.cascPath)
        self.recognizer = cv2.face.LBPHFaceRecognizer_create(radius=1,neighbors=8,grid_x=8,grid_y=8)
        self.students = [0]*len(arrayStudentObjects)  #assume all students are absent first
        self.numTrainPerFace = [0]*len(arrayStudentObjects)
        self.size = size

    def processImageAndGetConfidenceMatrix(self):
        #do not need to crop portraits anymore they should already be cropped from the db
        #self.cropPortraits()
        #print("cropped portraits")
        
        depthProcess = DepthProcessing(self.meeting, self.arrayStudents, self.size)
        depthProcess.beginDepthProcessing()
        #print("croppedMeetingPic")

        portraits, labels = self.prepareTraining(self.meeting.getPortraitsCroppedDirectory())
        #print("got portraits and labels")

        self.numTrainImgPerFace(labels)
        #print("got num trained per face")

        self.recognizer.train(portraits, numpy.array(labels))
        #print("trained recognizer")

        confMatrix = self.recognize(self.meeting.crops_directory)
        #print("got confidence matrix")
        return confMatrix

    def savePortraits(self):
        portraitsPath = self.meeting.getPortraitsDirectory()
        for student in self.arrayStudents:
            ascii = 97
            for portrait in student.portraits:
                cv2.imwrite(portraitsPath + "//" + str(student.getId()) + "." + chr(ascii) + ".jpg", portrait)
                ascii += 1

    def cropPortraits(self):
        
        path = self.meeting.getPortraitsDirectory() + '/*.jpg'
        i = 0
        for fname in glob.glob(path):
            #print(fname)
            picName = os.path.basename(os.path.normpath(fname))
            image = cv2.imread(fname)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self.faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=10, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cropImg = image[y:y + h, x:x + w]
                gray = cv2.cvtColor(cropImg, cv2.COLOR_BGR2GRAY)  # turn portrait to grayscale
                shrink = cv2.resize(gray, (self.size, self.size))
                cv2.imwrite(self.meeting.getPortraitsCroppedDirectory() + "//" + picName, shrink)
                #print("Cropped image " + picName)
                i += 1

    def detectAndCropMeetingPic(self):
        imagePath = self.meeting.getMeetingPicPath() #class picture
        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=10, minSize=(30, 30))

        #crops all faces from the class picure and saves them locally
        i=0
        for (x, y, w, h) in faces:
            cropImg = image[y:y+h, x:x+w]
            gray = cv2.cvtColor(cropImg, cv2.COLOR_BGR2GRAY)  # turn portrait to grayscale
            shrink = cv2.resize(gray, (self.size, self.size))
            strnum = str(i)
            if(len(strnum) == 1):
                strnum = "0"+strnum
            cv2.imwrite(self.meeting.getCropsDirectory()+"//"+str(strnum)+'.jpg', shrink)
            i += 1

    def prepareTraining(self, path):
        portraitList = [os.path.join(path,f) for f in os.listdir(path)]  #put portrait faces in a list
        portraits = []
        labels = []

        for i in portraitList:
            img = cv2.imread(i)    #read in a portrait
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  #turn portrait to grayscale
            shrink = cv2.resize(gray, (self.size,self.size))
            array = numpy.array(shrink, 'uint8')  #uint8 means unsigned int (0-255)

            filename = os.path.split(i)[1].split(".")[0]
            #num = os.path.basename(portraitPath)
            #print(num)

            portraits.append(array)  #add portrait to an array
            labels.append(int(filename))       #add matching student number to another array
            #smaller = cv2.resize(array, (0, 0), fx=0.3, fy=0.3)
            smaller = cv2.resize(array, (self.size,self.size))
            #cv2.imshow("Adding faces to training...", smaller)

            #cv2.waitKey(100)
        return portraits, labels

    def numTrainImgPerFace(self, labels):
        for i in range(len(labels)):
            self.numTrainPerFace[labels[i]] += 1

    def recognize(self, crop):

        collector = cv2.face.StandardCollector_create()
        confMatrix = []
        getMinConf = []
        min = 1000
        size = 0

        cropList = [os.path.join(crop, f) for f in os.listdir(crop)]  #put detected faces in a list
        baseAttendanceDict = {}
        faceNum=1
        for i in cropList:
            outerLoop = 0
            cropImg = cv2.imread(i)                           #read in a cropped image
            #cv2.imshow("Title", cropImg)
            cv2.waitKey(500)
            gray = cv2.cvtColor(cropImg, cv2.COLOR_BGR2GRAY)
            fixSize = cv2.resize(gray, (self.size,self.size))
            predictImg = numpy.array(fixSize, 'uint8')        #turn into numpy array

            numActual = int(os.path.split(i)[1].split(".")[0])
            numPredicted, conf = self.recognizer.predict(predictImg)

            self.recognizer.predict_collect(predictImg, collector)
            array1D = collector.getResults()
        

            #get only the confidence value in each tuple
            getConf = [x for _, x in array1D]
            #print(getConf)

            #find min conf value for each face
            #print("For Student " + str(count))

            for j in range(len(getConf)):
                size += 1

                temp = getConf[j]
                if(min > temp):
                    min = temp

                if(size == self.numTrainPerFace[outerLoop]):  #2 is numTrainPerFace
                    dist = min
                    getMinConf.append(dist)
                    min=1000
                    size=0
                    outerLoop+=1

            #print(getMinConf)

            confMatrix.append(getMinConf)
            getMinConf = []  #empty the list

            baseAttendanceDict[i] = numPredicted
            if numActual == numPredicted:
                print("{} Correctly matched as {}. conf {}".format(numActual, numPredicted, conf))
            else:
                print("{} wrongly recognized as {}. conf {}".format(numActual, numPredicted, conf))

            #cv2.waitKey(100)
            faceNum+=1

        #print()
        #confMatrix = '\n'.join([str(i) for i in confMatrix])
        confMatrix = numpy.array(confMatrix)  #2d list (list of lists) -> 2d matrix
        #print(confMatrix)
        #print(confMatrix[1][7])

        #print("done confidence:")
        #for i in range(len(confMatrix)):
        #    print(confMatrix[i])

        numberDetetedFaces = len(confMatrix)
        numberActualStudents = len(self.arrayStudents)

        #while (numberDetetedFaces > numberActualStudents):
        #    currentHightest = 0
        #    currentHighestCroppedNum = -1
        #    for i in range(len(confMatrix)):
        #        for j in range(len(confMatrix[0])):
        #            if(confMatrix[i][j] > currentHightest):
        #                currentHightest = confMatrix[i][j]
        #                currentHighestCroppedNum = i
        #    confMatrix = numpy.delete(confMatrix, currentHighestCroppedNum, 0)
        #    numberDetetedFaces -= 1




        return confMatrix

     


