class StudentMap:
    def __init__(self, studentObjectList):
        self.emailOf = {}
        self.codeforcesIdOf = {}
        self.objectOfId = {}
        self.objectOfUsername = {}
        self.usernames = set()

        for studentObject in studentObjectList:
            mail = studentObject.email
            uname = studentObject.username
            self.usernames.add(uname)
            self.emailOfUsername[uname] = mail
            self.codeforcesIdOfMail[mail] = uname
            self.objectOfMail[mail] = studentObject
            self.objectOfUsername[uname] = studentObject

    def usernameIsStudent(self, username):
        return username in self.usernames

    def getStudentFromUsername(self, username):
        return self.objectOfUsername[username]
