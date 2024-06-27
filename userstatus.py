import api
from submission import Submission

class UserStatus:
    def __init__(self, username, startTime, endTime):
        self.api_resp = api.apiResponse('user.status', {'handle': username}) 
        self.submissions = []
        self.acceptedProblemSubmissions = {}
        self.hasSkippedSubmissions = False
        for submissionJson in self.api_resp:
            submission = Submission(submissionJson)
            if submission.timestamp < startTime:
                break
            if submission.timestamp > endTime:
                continue
            self.submissions.append(submission)
            if submission.isAC and submission.problemID not in self.acceptedProblemSubmissions:
                self.acceptedProblemSubmissions[submission.problemID] = submission
            if submission.isSkipped:
                self.hasSkippedSubmissions = True
