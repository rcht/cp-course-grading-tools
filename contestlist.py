from constants import cp2StartTime, cp1EndTime
from api import apiResponse
from contest import Contest

class ContestList:
    def __init__(self, startTime = cp2StartTime, endTime = cp1EndTime):
        self.allContests = apiResponse('contest.list', {"gym":"false"})
        self.startTime = startTime
        self.endTime = endTime

        self.durationContests = []
        self.contestOfId = {}

        for contestJson in self.allContests:
            contest = Contest(contestJson)
            if not contest.isFinished:
                continue
            if contest.startTime < self.startTime:
                break
            self.contestOfId[contest.id] = contest
            self.durationContests.append(contest)

    def isValidContest(self, contestId):
        return contestId in self.contestOfId

    def contestFromId(self, contestId):
        return self.contestOfId[contestId]

    def contestList(self):
        return self.durationContests
