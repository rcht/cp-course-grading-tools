class StudentMap:
    def __init__(self, studentObjectList):
        self.emailOf = {}
        self.codeforcesIdOf = {}
        self.objectOfId = {}
        self.objectOfUsername = {}
        self.usernames = set()
        self.objectList = []
        self.emailOfUsername = {}
        self.codeforcesIdOfMail = {}
        self.objectOfMail = {}

        for studentObject in studentObjectList:
            mail = studentObject.email
            uname = studentObject.codeforcesUsername
            self.usernames.add(uname)
            self.emailOfUsername[uname] = mail
            self.codeforcesIdOfMail[mail] = uname
            self.objectOfMail[mail] = studentObject
            self.objectOfUsername[uname] = studentObject
            self.objectList.append(studentObject)

    def usernameIsStudent(self, username):
        return username in self.usernames

    def getStudentFromUsername(self, username):
        return self.objectOfUsername[username]

    def getStudentObjects(self):
        return self.objectList
