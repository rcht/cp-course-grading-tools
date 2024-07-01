class Contest:
    def __init__(self, contestJson):
        self.id = contestJson["id"]
        self.name = contestJson['name']
        self.isFinished = (contestJson['phase'] == 'FINISHED')
        self.hasStartTime = ('startTimeSeconds' in contestJson)
        self.hasDuration = ('durationSeconds' in contestJson)
        self.startTime = 0 if (not self.hasStartTime) else contestJson['startTimeSeconds']
        self.durationSeconds = 1 if (not self.hasDuration) else contestJson['durationSeconds'] 
        self.endTime = self.startTime + self.durationSeconds - 1


        self.isDiv4 = "Div. 4" in self.name 

        self.isDiv3 = (not self.isDiv3) and ("Educational" in self.name or "Div. 3" in self.name)

        self.isDiv2 = ("Div. 2" in self.name or "Global" in self.name) and (not self.isDiv3)

        # I wish there was a better solution but unfortunately not
        # There is no objectively correct way to get the rating division of a contest

         
