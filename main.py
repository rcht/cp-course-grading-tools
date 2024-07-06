from constants import *
from student import Student
from studentmap import StudentMap
from contestlist import ContestList
from studentupdater import StudentUpdater

import csv

# Fetch all emails and form responses
cp1RegsFile = open('cp1_final.csv')
cp2RegsFile = open('cp2_final.csv')
formRespFile = open('form_resp.csv')

mailCount = {}
idOf = {}

cp1Reader = csv.DictReader(cp1RegsFile)
cp2Reader = csv.DictReader(cp2RegsFile)
formRespReader = csv.DictReader(formRespFile)

for row in cp1Reader:
    nm = row['Email Id']
    mailCount[nm] = 1

for row in cp2Reader:
    nm = row['Email Id']
    mailCount[nm] = mailCount.get(nm,0) + 2

for row in formRespReader:
    nm = row['Email Address']
    cf_id = row['Codeforces user ID']
    idOf[nm] = cf_id

cp1RegsFile.close()
cp2RegsFile.close()
formRespFile.close()

studentObjects: list[Student] = []

for email in idOf:
    if not (email in mailCount):
        print("NO_ID", email)
    handle = idOf[email]
    if email not in mailCount:
        print("NOT_IN_COURSE", email)
        continue
    if mailCount[email] == 1:
        # CP1 Student
        obj = Student(email, handle)
    elif mailCount[email] == 2:
        # CP2 Student
        obj = Student(email, handle, div2Limit=cp2Div2Limit, div3Limit=cp2Div3Limit, ratingBase=cp2RatingBase, startTime=cp2StartTime, endTime=cp2EndTime, isCP2=True)
    else:
        # Both student
        obj = Student(email, handle, startTime=cp2StartTime, hasBoth=True)
    studentObjects.append(obj)


studentMap = StudentMap(studentObjects)
contestList = ContestList()
studentUpdater = StudentUpdater(studentMap, contestList)

studentUpdater.updateAllDiv2Points()
studentUpdater.updateInContestDiv3Points()
studentUpdater.updateInContestDiv4Points()
studentUpdater.updateStatuses()
studentUpdater.addAllLabs()

cp1OutputFile = open('cp1_tracker.csv', 'w')
cp2OutputFile = open('cp2_tracker.csv', 'w')
bothOutputFile = open('both_tracker.csv', 'w')

cp1Fieldnames = ["Email", "Codeforces Handle", "Div 2 Points", "Div 3 Points", "Practice Points", "Lab 1", "Lab 2", "Lab 3"]
cp2Fieldnames = cp1Fieldnames
bothFieldnames = ["Email", "Codeforces Handle", div2CP1Header, div3CP1Header, div2CP2Header, div3CP2Header, cp1PracticePointsHeader, cp2PracticePointsHeader,
                  "CP1 Lab 1", "CP1 Lab 2", "CP1 Lab 3",
                  "CP2 Lab 1", "CP2 Lab 2", "CP2 Lab 3"]


cp1Writer = csv.DictWriter(cp1OutputFile, fieldnames=cp1Fieldnames)
cp1Writer.writeheader()
cp2Writer = csv.DictWriter(cp2OutputFile, fieldnames=cp2Fieldnames)
cp2Writer.writeheader()
bothWriter = csv.DictWriter(bothOutputFile, fieldnames=bothFieldnames)
bothWriter.writeheader()

for student in studentObjects:
    toWrite = {"Email": student.email, "Codeforces Handle": student.codeforcesUsername}
    if student.hasBoth:
        # CF
        toWrite[cp1PracticePointsHeader] = student.practiceScore
        toWrite[cp2PracticePointsHeader] = student.additionalPracticePoints
        toWrite[div2CP1Header] = student.div2Score
        toWrite[div3CP1Header] = student.additionalDiv2Score
        toWrite[div2CP2Header] = student.div3Score
        toWrite[div3CP2Header] = student.additionalDiv3Score

        # Lab
        toWrite["CP1 Lab 1"] = sum(student.labScores.get("CP1 Lab 1", {}).values())
        toWrite["CP1 Lab 2"] = sum(student.labScores.get("CP1 Lab 2", {}).values())
        toWrite["CP1 Lab 3"] = sum(student.labScores.get("CP1 Lab 3", {}).values())
        toWrite["CP2 Lab 1"] = sum(student.labScores.get("CP2 Lab 1", {}).values())
        toWrite["CP2 Lab 2"] = sum(student.labScores.get("CP2 Lab 2", {}).values())
        toWrite["CP2 Lab 3"] = sum(student.labScores.get("CP2 Lab 3", {}).values())

        # to CSV
        bothWriter.writerow(toWrite)
    else:
        # CF
        toWrite["Div 2 Points"] = student.div2Score
        toWrite["Div 3 Points"] = student.div3Score
        toWrite["Practice Points"] = student.practiceScore
        
        # Lab
        if student.isCP2:
            toWrite["Lab 1"] = sum(student.labScores.get("CP2 Lab 1", {}).values())
            toWrite["Lab 2"] = sum(student.labScores.get("CP2 Lab 2", {}).values())
            toWrite["Lab 3"] = sum(student.labScores.get("CP2 Lab 3", {}).values())
        else:
            toWrite["Lab 1"] = sum(student.labScores.get("CP1 Lab 1", {}).values())
            toWrite["Lab 2"] = sum(student.labScores.get("CP1 Lab 2", {}).values())
            toWrite["Lab 3"] = sum(student.labScores.get("CP1 Lab 3", {}).values())

        # to CSV
        if student.isCP2:
            cp2Writer.writerow(toWrite)
        else:
            cp1Writer.writerow(toWrite)

cp1OutputFile.close()
cp2OutputFile.close()
bothOutputFile.close()
