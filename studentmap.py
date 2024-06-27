class StudentMap:
    def __init__(self, studentObjectList):
        self.emailOf = {}
        self.codeforcesIdOf = {}
        self.objectOfId = {}
        self.objectOfUsername = {}

        for studentObject in studentObjectList:
            mail = studentObject.email
            uname = studentObject.username
            self.emailOf[uname] = mail
            self.codeforcesIdOf[mail] = uname
            self.objectOfId[mail] = studentObject
            self.objectOfUsername[uname] = studentObject


