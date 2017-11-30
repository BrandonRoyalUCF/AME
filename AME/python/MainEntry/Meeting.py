class Meeting():
    
    def __init__(self, id, meetingPicPath, depthPicPath, meeting_directory, crops_directory, portraits_directory, portraits_cropped_directory, firstMeeting, countMeetings):
        self.id = id
        self.meetingPicPath = meetingPicPath
        self.depthPicPath = depthPicPath
        self.socialData = []
        self.meeting_directory = meeting_directory
        self.crops_directory = crops_directory
        self.portraits_directory = portraits_directory
        self.portraits_cropped_directory = portraits_cropped_directory
        self.averageSocialMatrix = []
        self.classNumToStudentIdDict = {} #key is the class num, value is the student id
        self.studentIdToClassNumDict = {} #key is the student id, value is the class num
        self.unrecognizedSocialMatrix = []
        self.croppedFaces = []
        self.firstMeeting = firstMeeting
        self.countMeetings = countMeetings
        self.countTotalStudents = 0
        self.matchDictionary = {} #key is the student class num, value is the matched cropped face number
        self.finalMatches = [] #index = the cropped face number, value is the student class num

    def getMeetingPicPath(self):
        return self.meetingPicPath

    def getDepthPicPath(self):
        return self.depthPicPath

    def getSocialData(self):
        return self.socialData

    def setSocialData(self, socialMatrix):
        self.socialData = socialMatrix

    def setMeetingDirectory(self, meeting_directory):
        self.meeting_directory = meeting_directory

    def setCropsDirectory(self, crops_directory):
        self.crops_directory = crops_directory

    def setPortraitsDirectory(self, portraits_directoy):
        self.portraits_directoy = portraits_directoy

    def getMeetingDirectory(self):
        return self.meeting_directory
    
    def getCropsDirectory(self):
        return self.crops_directory

    def getPortraitsDirectory(self):
        return self.portraits_directory

    def getPortraitsCroppedDirectory(self):
        return self.portraits_cropped_directory

    def setClassNumToStudentIdDict(self, dictionary):
        self.classNumToStudentIdDict = dictionary

    def getClassNumToStudentIdDict(self):
        return self.classNumToStudentIdDict

    def setStudentIdToClassNumDict(self, dictionary):
        self.studentIdToClassNumDict = dictionary

    def getStudentIdToClassNumDict(self):
        return self.studentIdToClassNumDict

    def setUnrecognizedSocialMatrix(self, matrix):
        self.unrecognizedSocialMatrix = matrix

    def getUnrecognizedSocialMatrix(self):
        return self.unrecognizedSocialMatrix

    def setCroppedFaces(self, croppedFaces):
        self.croppedFaces = croppedFaces
    
    def getCroppedFaces(self):
        return self.croppedFaces

    def getFirstMeeting(self):
        return self.firstMeeting

    def getCountMeetings(self):
        return self.countMeetings

    def getCountTotalStudents(self):
        return self.countTotalStudents

    def setCountTotalStudents(self, count):
        self.countTotalStudents = count

    def setAverageSocialMatrix(self, matrix):
        self.averageSocialMatrix = matrix

    def getAverageSocialMatrix(self):
        return self.averageSocialMatrix

    def setMatchDictionary(self, dict):
        self.matchDictionary = dict

    def getMatchDictionary(self):
        return self.matchDictionary

    def getFinalMatches(self):
        return self.finalMatches

    def setFinalMatches(self, matches):
        self.finalMatches = matches



