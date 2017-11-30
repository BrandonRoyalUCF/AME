class Student():
    
    def __init__(self, id, classNumber, firstName, lastName, socialData):
        self.id = id
        self.classNumber = classNumber
        self.firstName = firstName
        self.lastName = lastName
        #self.portraits = portraits
        self.socialData = socialData
        self.present = False
        self.croppedFaceMatchPath = ""
        self.croppedFaceMatchId = -1
        self.matchedSocialArray = []
        

    def getId(self):
        return self.id

    def getClassNumber(self):
        return self.classNumber

    def getFullName(self):
        full = self.firstName + " " + self.lastName
        return full

    def getSocialData(self):
        return self.socialData

    def setCroppedFaceMatchId(self, id):
        self.croppedFaceMatchId = id

    def getCroppedFaceMatchId(self):
        return self.croppedFaceMatchId

    def setPresent(self, present):
        self.present = present

    def getPresent(self):
        return self.present

    def setCroppedFaceMatchPath(self, path):
        self.croppedFaceMatchPath = path

    def getCroppedFaceMatchPath(self):
        return self.croppedFaceMatchPath





