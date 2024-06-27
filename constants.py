from datetime import datetime
from time import mktime

def unixTime(*args):
    dt = datetime(*args)
    return int(mktime(dt.timetuple()))

cp2StartTime = unixTime(2024, 5, 31, 0, 0, 0) # start of 31st May 2024
cp2EndTime = unixTime(2024, 7, 20, 23, 59, 59) # end of 20th July 2024
cp1StartTime = unixTime(2024, 6, 3, 0, 0, 0) # start of 3rd July 2024  
cp1EndTime = cp2EndTime

div2CP1Header = "Div. 2 Points (CP1)"
div2CP2Header = "Div. 2 Points (CP2)"
div3CP1Header = "Div. 3 Points (CP1)"
div3CP2Header = "Div. 3 Points (CP2)"

cp1PracticePointsHeader = "Practice Points (CP1)"
cp2PracticePointsHeader = "Practice Points (CP2)"

cp1PracticeLimit = 50
cp2PracticeLimit = 50

cp1RatingBase = 1000
cp2RatingBase = 1200

def pointsOf(rating, base):
    if rating < base:
        return 0
    else:
        return 1 + (rating - base)//200

cp1Div2Limit = 3000
cp2Div2Limit = 4000

cp1Div3Limit = 10
cp2Div3Limit = 15

cp1Div4Multiplier = 1
cp2Div4Multiplier = 0.75

lab1Label = "Lab 1 score (/10)"
lab2Label = "Lab 2 score (/10)"
lab3Label = "Lab 3 score (/10)"
lab4Label = "Lab 4 score (/10)"

currentCP1Headers = [div2CP1Header, div3CP1Header, cp1PracticePointsHeader]
currentCP2Headers = [div2CP2Header, div3CP2Header, cp2PracticePointsHeader]
currentCombinedHeaders = currentCP1Headers + currentCP2Headers


