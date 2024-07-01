from api import apiResponse
from ranklistrow import RanklistRow

class Standings:
    def __init__(self, contestId):
        standingsJson = apiResponse('contest.standings', {'contestId': str(contestId)}) 
        self.rows = []
        for row in standingsJson['rows']:
            self.rows.append(RanklistRow(row))
    def rows(self):
        return self.rows
