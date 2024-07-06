class RanklistRow:
    def __init__(self, rankListRowJson):
        self.handle = rankListRowJson["party"]["members"][0]["handle"].lower()
        self.points = int(rankListRowJson["points"])
        indOrd = ord('A')
        self.solvedIndices = []
        for problemResult in rankListRowJson["problemResults"]:
            pts = int(problemResult["points"])
            if pts > 0:
                self.solvedIndices.append(chr(indOrd))
            indOrd += 1
