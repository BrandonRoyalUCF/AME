import cv2
import os
import numpy
#from PIL import Image
#import matplotlib.pyplot as plt


#imagePath = "portraitsOrig/7.jpg"

#recognizer = cv2.face.EigenFaceRecognizer_create()
#recognizer = cv2.face.FisherFaceRecognizer_create(num_components=10000, threshold=5000)

#image = cv2.imread(imagePath)
#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#15 needed SF=1.2 to detect portrait
#4 needed SF=1.1 and mN=5 to detect portrait
#faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=10, minSize=(30, 30))

#print("Found {0} faces!".format(len(faces)))

#students = [0]*15  #assume all students are absent first
#numTrainPerFace = [0]*15

#for our visual purposes. has green rectangle around detected faces

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
recognizer = cv2.face.LBPHFaceRecognizer_create(radius=1,neighbors=8,grid_x=8,grid_y=8)


def detectTest():
    imagePath = "IMG_3123.jpg"
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=10, minSize=(30, 30))

    print("Found {0} faces!".format(len(faces)))

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 10)
    cv2.imwrite("detection.jpg", image)


#only need to run this. no green rectangles
def detectAndCrop(pathMeetingPic, directory):
    imagePath = pathMeetingPic
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=10, minSize=(30, 30))

    i=0
    for (x, y, w, h) in faces:
        cropImg = image[y:y+h, x:x+w]
        gray = cv2.cvtColor(cropImg, cv2.COLOR_BGR2GRAY)  # turn portrait to grayscale
        shrink = cv2.resize(gray, (500, 500))
        cv2.imwrite(directory + '//CroppedFaces//face'+str(i)+'.png', shrink)
        i += 1


#train recognizer with the portraits
def prepareTraining(path):
    portraitList = [os.path.join(path,f) for f in os.listdir(path)]  #put portrait faces in a list
    portraits = []
    labels = []

    for i in portraitList:
        img = cv2.imread(i)    #read in a portrait
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  #turn portrait to grayscale
        shrink = cv2.resize(gray, (500,500))
        array = numpy.array(shrink, 'uint8')  #uint8 means unsigned int (0-255)

        num = int(os.path.split(i)[1].split(".")[0])
        #num = os.path.basename(portraitPath)
        print(num)

        portraits.append(array)  #add portrait to an array
        labels.append(num)       #add matching student number to another array
        #smaller = cv2.resize(array, (0, 0), fx=0.3, fy=0.3)
        smaller = cv2.resize(array, (200,200))
        #cv2.imshow("Adding faces to training...", smaller)

        cv2.waitKey(100)

    return portraits, labels


#perform face recognition
def recognize(crop):
    #matrix = numpy.zeros((15, 15))
    collector = cv2.face.StandardCollector_create()
    confMatrix = []
    getMinConf = []
    min = 1000
    size = 0

    cropList = [os.path.join(crop, f) for f in os.listdir(crop)]  #put detected faces in a list

    faceNum=1
    for i in cropList:
        outerLoop = 0
        cropImg = cv2.imread(i)                           #read in a cropped image
        gray = cv2.cvtColor(cropImg, cv2.COLOR_BGR2GRAY)
        fixSize = cv2.resize(gray, (500,500))
        predictImg = numpy.array(fixSize, 'uint8')        #turn into numpy array

        numActual = int(os.path.split(i)[1].split(".")[0])
        #numPredicted, conf = recognizer.predict(predictImg)

        recognizer.predict_collect(predictImg, collector)
        array1D = collector.getResults()
        print(array1D)

        #get only the confidence value in each tuple
        getConf = [x for _, x in array1D]
        print(getConf)

        #find min conf value for each face
        for j in range(len(getConf)):
            size += 1

            temp = getConf[j]
            if(min > temp):
                min = temp

            if(size == 2):  #2 is numTrainPerFace
                dist = min
                getMinConf.append(dist)
                min=1000
                size=0

        #print minConf
        confMatrix.append(getMinConf)
        getMinConf = []  #empty the list
        outerLoop += 1

        #newMatrix = numpy.column_stack(getConf)
        #newMatrix = numpy.stack(getConf)
        #recognizer.addNums()

        '''
        if numActual == numPredicted:
            print("{} correctly recognized as {}. conf {}".format(numActual, numPredicted, conf))
            students[numPredicted-1] = 1
        else:
            print("{} wrongly recognized as {}. conf {}".format(numActual, numPredicted, conf))
        '''

        ##part of checkPresent
        #student[numPredicted].append(1)  can use either, i think
        #student[numPredicted] = 1

        bigger = cv2.resize(predictImg, (200, 200))
        #cv2.imshow("Recognizing Face", bigger)
        #cv2.imwrite('trash/f' + str(faceNum) + '.jpg', bigger)
        cv2.waitKey(100)
        faceNum+=1

    print()
    #confMatrix = '\n'.join([str(i) for i in confMatrix])
    confMatrix = numpy.array(confMatrix)  #2d list (list of lists) -> 2d matrix
    print(confMatrix)
    print(confMatrix[1][7])
    return confMatrix


def checkPresent():
    print(students)
    for i in range(len(students)):
        if students[i] == 1:
            print("student {} present".format(i+1))
        else:
            print("student {} absent".format(i+1))


def numTrainImgPerFace(labels):
    for i in range(len(labels)):
        numTrainPerFace[labels[i]] += 1
    #print(numTrainPerFace)

def mainStart(arrayStudentIds, pathMeetingPic, arrayOfStudentPicPaths, directory):

    '''Like a Main function below'''
    detectAndCrop(pathMeetingPic, directory)
    #detectTest()

    path = directory + '//studentPics'
    portraits, labels = prepareTraining(path)

    print("portraitLabels:", labels)
    numTrainImgPerFace(labels)
    cv2.destroyAllWindows()

    recognizer.train(portraits, numpy.array(labels))

    crop = directory + '//CroppedFaces'
    confMatrix = recognize(crop)

    return confMatrix

#checkPresent()


'''
print("\n")
matrix = numpy.zeros((5,5))  #5x5 matrix with all 0's
print(matrix)

matrix2 = numpy.array([[1,2,3],[7,8,9]])
print(matrix2)
print(matrix2[0,2])  #row 0, col 2
'''




'''
#Depth Map attempt
#imgR = cv2.imread("Yeuna9x.png")
#imgL = cv2.imread("SuXT483.png")
imgR = cv2.imread("4-L.jpg")
imgL = cv2.imread("4-R.jpg")

imgR_new = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)
imgL_new = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
#cv2.imshow("imgR", imgR_new)

stereo = cv2.StereoBM_create(numDisparities=16, blockSize=7)
disparity = stereo.compute(imgL_new, imgR_new)

plt.imshow(disparity, 'gray')
#plt.xticks([])
#plt.yticks([])
plt.show()

#cv2.imshow("Depth Map", disparity)
cv2.waitKey(0)
'''


'''
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

imagePath = "IMG_3123.jpg"
image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=10, minSize=(30, 30))

print("Found {0} faces!".format(len(faces)))

i=1
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 10)
    cv2.circle(image, center=((int)(x+w/2),(int)(y+h/2)) ,radius=5, color=(0,0,255), thickness=-1)
    cv2.putText(image, 'F'+str(i), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,255), 5)
                                                                  #fontsize          #thickness
    print("F{}- xCoord:{}, yCoord:{}".format(str(i), (int)(x+w/2), (int)(y+h/2)))  #key part
    i+=1

bigger = cv2.resize(image, (0,0), fx=.3, fy=.3)
cv2.imshow("img", bigger)
#cv2.imwrite("center.jpg", image)
cv2.waitKey(0)
'''

'''max contour approach doesn't work 
def findMarker(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 35, 125)
    resize = cv2.resize(edged, (0, 0), fx=.2, fy=.2)
    #cv2.imshow("edged", resize)
    (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    c = max(cnts, key=cv2.contourArea)
    return cv2.minAreaRect(c)

imagePath = "ref.jpg"
image = cv2.imread(imagePath)
marker = findMarker(image)

box = numpy.int0(cv2.boxPoints(marker))
cv2.drawContours(image, [box], -1, (0, 255, 0), 2)

resize = cv2.resize(image, (0,0), fx=.2, fy=.2)
cv2.imshow("edged", resize)
cv2.waitKey(0)
'''

'''
img1 = cv2.imread("refobj.jpg")
img2 = cv2.imread("refb.jpg")  //when using orb, images can be whatever size it seems

orb = cv2.ORB_create()
kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

matches = bf.match(des1,des2)
matches = sorted(matches, key = lambda x:x.distance)

img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:10], None,flags=2)
plt.imshow(img3)
plt.show()
'''


'''don't think features will work since the big x has very few actual features
img1 = cv2.imread("refobj.jpg")  #train
img2 = cv2.imread("refb.jpg")   #query. when using sift, images can't be too big.

sift = cv2.xfeatures2d.SIFT_create()

FLANN_INDEX_KDTREE = 0
flannParam = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
#search_params = dict(checks = 50)

flann = cv2.FlannBasedMatcher(flannParam, {})

kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)
matches = flann.knnMatch(des1,des2,k=2)

MIN_MATCH_COUNT=30
good = []
for m,n in matches:
    if m.distance < 0.7*n.distance:
        good.append(m)
if len(good)>MIN_MATCH_COUNT:
    src_pts = numpy.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = numpy.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()

    h,w = img1.shape
    pts = numpy.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,M)

    img2 = cv2.polylines(img2,[numpy.int32(dst)],True,255,3, cv2.LINE_AA)

else:
    print ("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
    matchesMask = None

draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                   singlePointColor = None,
                   matchesMask = matchesMask, # draw only inliers
                   flags = 2)

img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)
plt.imshow(img3, 'gray')
plt.show()
'''

'''
cascPath2 = "haarcascade_frontalcatface_extended.xml"
carCascade = cv2.CascadeClassifier(cascPath2)

imagePath = "ref3.jpg"  #cat face should be neutral. angry doesn't work
image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)      #1.2             #10
cat = carCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=1, minSize=(1, 1))
face = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

print(cat)
#print(face)
print("Found {0} cat!".format(len(cat)))
#print("Found {0} face!".format(len(face)))

indicesToDel = []
i=0
for (x,y,w,h) in cat:
    for (x2,y2,w2,h2) in face:
        if(abs(x-x2) < 100):   #25
            indicesToDel.append(i)
            break
    i+=1

print(indicesToDel)
newCat = numpy.delete(cat,indicesToDel,axis=0)
print(newCat)


knownDist = 52.0
knownWidth = 7.5  #minus 1in since detected cat face isn't whole width of paper
knownFocal = 2218.67

for (x,y,w,h) in newCat:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0,0,255), 5)
    #cv2.line(image, (x+w,y+h), (x,y+h), color=(0, 0, 0), thickness=10)
    #print((x+w,y+h))
    #print((x,y+h))
    pixelWidth = w
    print(((int)(x+w/2),(int)(y+h/2)))

#focalLength = (pixelWidth*knownDist)/knownWidth
dist = (knownWidth*knownFocal)/pixelWidth
print("camDist: {}" .format(dist))

#find distance of all faces to camera
for (x,y,w,h) in face:
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 10)
    cv2.circle(image, center=((int)(x+w/2), (int)(y+h/2)), radius=10, color=(0,0,255), thickness=-1)
    pixelWidth = w
    dist = (knownWidth*knownFocal)/pixelWidth
    print(dist)
    print(((int)(x+w/2),(int)(y+h/2)))


#if (perA-perB < 50) #they're across from each other
#    abs(perAx-perBx)
#else  #they're behind each other
#    perA-perB


bigger = cv2.resize(image, (800, 600))
cv2.imshow("img", bigger)
cv2.waitKey(0)
#plt.imshow(image)
#plt.show()
'''


##########################################################################################


'''
rectangle(para1,para2,para3,para4,para5)
para1 is source file
para2 is point1 of rectangle
para3 is point2 of rectangle opposite to point1
para4 is color of rectangle
para5 is width of the border. -1 to fill box entirely
'''

'''
    images = []
    portraits = glob.glob('portraits/*.jpg')
    for pics in portraits:
        img = cv2.imread(pics)
        images.append(img)

    print('images shape:', numpy.array(images).shape)
'''

#since our pics are very large, do .20 for the portraits, do .27 for the whole class
#smaller = cv2.resize(image, (0,0), fx=0.27, fy=0.27)
#cv2.imshow("Faces found", smaller)

#save picture or close window
'''
key = cv2.waitKey(0)
if key == ord('s'):
    cv2.imwrite("pic.jpg", smaller)
    cv2.destroyAllWindows()
else:
    cv2.destroyAllWindows()
'''