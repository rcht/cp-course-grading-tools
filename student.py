from submission import Submission
from userstatus import UserStatus
from ranklistrow import RanklistRow
from constants import *
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
                 isCP2 = False, 
                 hasBoth = False):

        '''
        @param email: Email ID of student. String.
        @param codeforcesUsername: Codeforces username of student. String.
        @param div2Limit: div 2 limit. Defaults to cp1 limit
        @param div3Limit: div 3 limit. Defaults to cp1 limit.
        @param startTime: starting unix timestamp of submissions considered. 
        @param endTime: ending unix timestamp of submissions considered. 
        @param ratingBase: base rating for practice problems. Defaults to cp1 base rating
        @param isCP2: boolean
        @param hasBoth: boolean
        '''

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

        # things for students who have taken both courses 
        self.hasBoth = hasBoth
        self.additionalDiv2Score = 0
        self.additionalDiv3Score = 0
        self.additionalPracticePoints = 0


    def addDiv2contest(self, ranklistRow: RanklistRow, contest: Contest):
        contestId = contest.id
        if contest.startTime < self.startTime or contest.startTime > self.endTime:
            return None
        if contestId in self.div2IDs:
            return None

        self.div2IDs.add(contestId)
        pts = ranklistRow.points

        ###
        if self.hasBoth:
            # both cp1 and cp2
            if self.div2Score < cp1Div2Limit:
                # if cp1 div 2 points pending
                self.div2Score += pts
                if self.div2Score >= cp1Div2Limit:
                    self.additionalDiv2Score += (self.div2Score - cp1Div2Limit)
                    self.div2Score = cp1Div2Limit
            else:
                # only cp2 div 2 points left
                self.additionalDiv2Score += pts
                self.additionalDiv2Score = min(self.additionalDiv2Score, cp2Div2Limit)
            return None
        ###

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
        
        ###
        if self.hasBoth:
            if self.div3Score < cp1Div3Limit:
                # cp1 div 3 points pending
                self.div3Score += pts
                if self.div3Score >= cp1Div3Limit:
                    self.additionalDiv3Score += (self.div3Score - cp1Div3Limit)
                    self.div3Score = cp1Div3Limit
            else:
                # cp2 points left
                if isDiv4:
                    self.additionalDiv3Score += pts * multiplier
                else:
                    self.additionalDiv3Score += pts
                self.additionalDiv3Score = min(self.additionalDiv3Score, cp2Div3Limit)
            return None
        ###

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

    def addOutOfContestPoint(self, isDiv4):

        ###
        if self.hasBoth:
            if self.div3Score < cp1Div3Limit:
                self.div3Score += 1
            else:
                if isDiv4:
                    self.additionalDiv3Score += cp2Div4Multiplier
                else:
                    self.additionalDiv3Score += 1
                self.additionalDiv3Score = min(self.additionalDiv3Score, cp2Div3Limit)
            return None
        ###

        if not isDiv4:
            self.div3Score += 1
        else:
            self.div3Score += (cp2Div4Multiplier if self.isCP2 else cp1Div4Multiplier)
        self.div3Score = min(self.div3Score, self.div3Limit)

    def addPracticeProblem(self, rating):

        ###
        if self.hasBoth:
            if self.practiceScore < cp1PracticeLimit:
                # cp1 practice points pending
                self.practiceScore += pointsOf(rating, self.ratingBase)
                if self.practiceScore >= cp1PracticeLimit:
                    self.additionalPracticePoints += (self.practiceScore - cp1PracticeLimit)
                    self.practiceScore = cp1PracticeLimit
                    self.ratingBase = cp2RatingBase
            else:
                self.additionalPracticePoints += pointsOf(rating, self.ratingBase)
                self.additionalPracticePoints = min(self.additionalPracticePoints, cp1PracticeLimit)
            return None
        ###

        self.practiceScore += pointsOf(rating, self.ratingBase)
        self.practiceScore = min(self.practiceScore, cp1PracticeLimit)

    def processStatus(self, contestList: ContestList):
        self.practiceScore = 0
        div3ContestsToAdd = set()

        try:
            userStatus = UserStatus(self.codeforcesUsername, self.startTime, self.endTime)

            for submission in userStatus.acceptedProblemSubmissions.values():
                # add problem of this rating to practice
                self.addPracticeProblem(submission.problemRating)
                if submission.problemRating >= 1800:
                    print("HIGH", self.email, self.codeforcesUsername)
                # check if it was an in-contest submission and the contest is not already added
                cid = submission.contestId
                if not contestList.isValidContest(cid):
                    continue
                contest = contestList.contestFromId(cid)
                if not (contest.isDiv4 or contest.isDiv3):
                    continue
                if cid in self.div3IDs:
                    continue
                if submission.contestRelativeSeconds >= contest.durationSeconds:
                    continue
                div3ContestsToAdd.add(cid)
                self.addOutOfContestPoint(contest.isDiv4)

            for i in div3ContestsToAdd:
                self.div3IDs.add(i)

            if userStatus.hasSkippedSubmissions:
                self.hasPlag = True
                print("SKIPPED", self.email, self.codeforcesUsername)

        except FailedRequestException:
            print("INVALID", self.email, self.codeforcesUsername)


class CombinedStudent(Student):
    pass
