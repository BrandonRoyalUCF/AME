#######################################################################################
#
#
# Script that is given student _id and array of attachment_ids and crops each portrait
#
#
#######################################################################################

import json
import sys
from gridfs import *
import cv2
from io import BytesIO
from pymongo import *
from bson.objectid import ObjectId
import numpy as np
import json
import os

jsonString = sys.argv[1]
jsonObject = json.loads(jsonString)
studentId = jsonObject['student_id']
attachmentIds = jsonObject['attachment_ids']

#attachmentIds = ['5a1eee79b2d9e60f404efb13']
#studentId = '5a1eee79b2d9e60f404efb07'

current_directory = os.getcwd()
crop_portraits_directory = os.path.join(current_directory, "cropThePortraits")
if not os.path.exists(crop_portraits_directory):
    os.makedirs(crop_portraits_directory)

client = MongoClient('mongodb://10.171.204.168:27017/')
db = client['test']
attachments = GridFS(db, collection = 'attachments')

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
err = None
try:
    for id in attachmentIds:

        #first read in the image and write it to a local directory
        portraitStream = attachments.get(ObjectId(id)).read()
        portraitPicNumpy = np.fromstring(portraitStream, np.uint8)
        portrait_img_np = cv2.imdecode(portraitPicNumpy, cv2.IMREAD_COLOR)
        path =  crop_portraits_directory + "\\" + str(id) + ".jpg"
        cv2.imwrite(path, portrait_img_np)
        print("Wrote image " + str(path))

        #now crop the image and write it back to the same location
        picName = os.path.basename(os.path.normpath(path))
        image = cv2.imread(path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=10, minSize=(30, 30))
        for (x, y, w, h) in faces:
                cropImg = image[y:y + h, x:x + w]
                gray = cv2.cvtColor(cropImg, cv2.COLOR_BGR2GRAY)  # turn portrait to grayscale
                shrink = cv2.resize(gray, (100, 100))
                cv2.imwrite(path, shrink)
                print("Cropped image " + picName)
    

        #delete the old image in the database
        #attachments.delete(ObjectId(id))

        #insert the new image and get its new id
        imagebytes = open(path, "rb").read()
        new_id = attachments.put(imagebytes, filename = 'CroppedPortrait.jpg')

        new_id_string = str(new_id)

        #add the new file id to the meeting
        students = db['students']
        students.update_one({"_id": ObjectId(studentId)},{"$push": {"studentPortraitAttachment_ids": new_id_string}})
except:
    err = sys.exc_info()[0]

sys.stdout.write(str(err))

