class Submission:
    def __init__(self, submissionJson):
        self.contestId = submissionJson["contestId"]
        self.timestamp = submissionJson["creationTimeSeconds"]
        self.handle = submissionJson["author"]["members"][0]["handle"]
        self.contestRelativeSeconds = submissionJson["relativeTimeSeconds"]
        self.verdict = submissionJson["verdict"]
        self.isAC = (self.verdict == 'OK')
        self.isSkipped = (self.verdict == 'SKIPPED')
        self.problem = submissionJson["problem"]
        self.problemRating = (0 if 'rating' not in self.problem else self.problem['rating']) 
        self.problemID = str(self.contestId) + self.problem["index"]
