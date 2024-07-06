from studentmap import StudentMap
from contestlist import ContestList
from standings import Standings

# from student import Student

class StudentUpdater:

    def __init__(self, studentMap: StudentMap, contestList: ContestList):
        self.studentMap = studentMap
        self.contestList = contestList

    def updateAllDiv2Points(self):
        for contest in self.contestList:
            if not contest.isDiv2:
                continue

            standings = Standings(contest.id)

            for ranklistrow in standings.rows:
                # Not a CP1/CP2 student
                uname = ranklistrow.handle
                if not self.studentMap.usernameIsStudent(uname):
                    continue
                # studentObject = Student()
                studentObject = self.studentMap.getStudentFromUsername(uname)
                studentObject.addDiv2contest(ranklistrow, contest)

    def updateInContestDiv3Points(self):
        for contest in self.contestList:
            if not contest.isDiv3:
                continue

            standings = Standings(contest.id)

            for ranklistrow in standings.rows:
                # Not a CP1/CP2 student
                uname = ranklistrow.handle
                if not self.studentMap.usernameIsStudent(uname):
                    continue
                # studentObject = Student()
                studentObject = self.studentMap.getStudentFromUsername(uname)
                studentObject.addDiv3contest(ranklistrow, contest)

    def updateInContestDiv4Points(self):

        for contest in self.contestList:
            if not contest.isDiv4:
                continue

            standings = Standings(contest.id)

            for ranklistrow in standings.rows:
                # Not a CP1/CP2 student
                uname = ranklistrow.handle
                if not self.studentMap.usernameIsStudent(uname):
                    continue
                # studentObject = Student()
                studentObject = self.studentMap.getStudentFromUsername(uname)

                if studentObject.isCP2:
                    studentObject.addDiv3contest(ranklistrow, contest, True, 0.75)
                else:
                    studentObject.addDiv3contest(ranklistrow, contest, True)

    def updateStatuses(self):

        for student in self.studentMap.getStudentObjects():

            student.processStatus(self.contestList)
