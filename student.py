from userstatus import UserStatus
from ranklistrow import RanklistRow
from constants import cp1Div2Limit, cp1Div3Limit, cp1StartTime, cp1EndTime, cp1RatingBase, pointsOf, cp1PracticeLimit
from exceptions import FailedRequestException
from contest import Contest
from contestlist import ContestList

class Student:

    def __init__(self, 
                 email:str, 
                 codeforcesUsername:str, 
                 div2Limit = cp1Div2Limit, 
                 div3Limit = cp1Div3Limit, 
                 startTime = cp1StartTime, 
                 endTime = cp1EndTime, 
                 ratingBase = cp1RatingBase,
                 isCP2 = False):

        self.email = email
        self.codeforcesUsername = codeforcesUsername.lower()
        self.div2Score = 0
        self.div3Score = 0
        self.practiceScore = 0
        self.div2IDs = set()
        self.div3IDs = set()
        self.div2Limit = div2Limit
        self.div3Limit = div3Limit
        self.labScores = {}
        self.startTime = startTime
        self.endTime = endTime
        self.hasPlag = False
        self.ratingBase = ratingBase
        self.isCP2 = isCP2
        pass

    def addDiv2contest(self, ranklistRow: RanklistRow, contest: Contest):
        contestId = contest.id
        if contest.startTime < self.startTime or contest.startTime > self.endTime:
            return None
        if contestId in self.div2IDs:
            return None
        self.div2IDs.add(contestId)
        pts = ranklistRow.points
        self.div2Score += pts
        self.div2Score = max(0, min(self.div2Score, self.div2Limit))

    def addDiv3contest(self, ranklistRow: RanklistRow, contest: Contest, isDiv4 = False, multiplier = 1):
        contestId = contest.id
        if contest.startTime < self.startTime or contest.startTime > self.endTime:
            return None
        if contestId in self.div3IDs:
            return None
        self.div3IDs.add(contestId)
        pts = ranklistRow.points
        if isDiv4:
            self.div3Score += pts * multiplier 
        else:
            self.div3Score += pts
        self.div3Score = max(0, min(self.div3Score, self.div3Limit))


    def addLab(self, labHeader: str, ranklistRow: RanklistRow, upsolve: bool = False):
        if labHeader not in self.labScores:
            self.labScores[labHeader] = {}
        for solvedProblem in ranklistRow.solvedIndices:
            self.labScores[labHeader][solvedProblem] = max(self.labScores[labHeader].get(solvedProblem, 0), 0.4 if upsolve else 1)

    def processStatus(self, contestList: ContestList):
        try:
            userStatus = UserStatus(self.codeforcesUsername, self.startTime, self.endTime)
            for submission in userStatus.acceptedProblemSubmissions.values():
                self.practiceScore += pointsOf(submission.problemRating, self.ratingBase)
            if self.practiceScore > cp1PracticeLimit:
                print("Extra points found for:", self.email, self.codeforcesUsername)
            self.practiceScore = min(cp1PracticeLimit, self.practiceScore)
            if userStatus.hasSkippedSubmissions:
                self.hasPlag = True

        except FailedRequestException:
            print("Invalid username for:", self.email)


class CombinedStudent(Student):
    pass
