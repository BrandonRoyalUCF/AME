import cv2

#print(cv2.__version__)

imagePath = "IMG_3164.jpg"
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

faces = faceCascade.detectMultiScale(gray, scaleFactor=1.30, minNeighbors=10, minSize=(30, 30))

print("Found {0} faces!".format(len(faces)))

'''
rectangle(para1,para2,para3,para4,para5)
para1 is source file
para2 is point1 of rectangle
para3 is point2 of rectangle opposite to point1
para4 is color of rectangle
para5 is width of the border. -1 to fill box entirely
'''

#for our visual purposes
def detect():
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 10)
    cv2.imwrite("detection.jpg", image)

#only need to run this
def crop():
    i=1
    for (x, y, w, h) in faces:
        cropImg = image[y:y+h, x:x+w]
        cv2.imwrite('crops/face'+str(i)+'.jpg', cropImg)
        i += 1

#detect()
crop()


########################################################################

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
