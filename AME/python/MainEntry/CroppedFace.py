class CroppedFace(object):
    
    def __init__(self, id, x, y, w, h, xd, yd, wd, hd, croppedImagePath, averageDepthGreyScale, faceMidPoint, distanceFromCamera):
        self.id = id
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.xd = xd
        self.yd = yd
        self.wd = wd
        self.hd = hd
        self.croppedImagePath = croppedImagePath
        self.recognized = False
        self.studentMatchId = -1
        self.studentMatchClassNum = -1
        self.studentMatchFullName = ""
        self.averageDepthGreyScale = averageDepthGreyScale
        self.faceMidPoint = faceMidPoint
        self.distanceFromCamera = distanceFromCamera

    def getId(self):
        return self.id

    def getOrginalCoordinates(self):
        return self.x, self.y, self.w, self.h
        
    def getDepthCoordinates(self):
        return self.xd, self.yd, self.wd, self.hd

    def getCroppedImagePath(self):
        return self.croppedImagePath

    def getReconized(self):
        return self.recognized

    def setRecognized(self, value):
        self.recognized = value

    def getStudentMatchId(self):
        return self.studentMatchId

    def setStudentMatchId(self, value):
        self.studentMatchId = value

    def setStudentMatchClassNum(self, value):
        self.studentMatchClassNum = value

    def getMidPoint(self):
        return self.faceMidPoint

    def getDistanceFromCamera(self):
        return self.distanceFromCamera

    def getStudentMatchFullName(self):
        return self.studentMatchFullName

    def setStudentMatchFullName(self, fullname):
        self.studentMatchFullName = fullname





