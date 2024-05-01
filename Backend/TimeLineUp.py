def main():
    pass
 
def GetTimes():
    """This is the function that gathers the times from the database"""
    pass



def CheckOverlap(RequestPerson,ReplyPeople,ReplyID,NumRequired,MeetingLen):
    """This function takes in the avalibilities of each person as a list of strings and finds overlap"""
    output = []
    #The following piece of code makes a list of the dates
    dates = []
    RequestDays = RequestPerson.split(".")
    for Day in RequestDays:
        Day = Day.split(":")
        dates.append(Day[0])
    
    #The following piece of code makes a list of all times split into 15 min incraments
    Times = []
    for hour in range(0,24):
        for min in ["00","15","30","45"]:
            Times.append([(str(hour) + min),[]])

    #This makes a dictionary with each date having the full list of times and spaces for data to be added
    DateTime = {}
    for DayNTime in dates:
        DateTime.update({DayNTime:Times.copy()})

    # Avert your eyes its hideous and innaficient
    #This chunk starts by isolating the time range for each day
    number = -1
    for person in ReplyPeople:
        number += 1
        DayTime = person.split(".")
        for Day in DayTime:
            date = Day.split(":")
            IndavidualTimes = date[1].split(",")
            indavidualTimes = []

            #This chunk is attempting to get all the times in the ranges into a list and spliting it into 15 min incraments
            for indavidualTime in IndavidualTimes:
                #getting the correct number of mins for the first hour
                if (int(indavidualTime[2:4]) == 0):
                    indavidualTimes.append(str(int(indavidualTime[0:2]))+"00")
                if (int(indavidualTime[2:4]) <= 15):
                    indavidualTimes.append(str(int(indavidualTime[0:2]))+"15")
                if (int(indavidualTime[2:4]) <= 30):
                    indavidualTimes.append(str(int(indavidualTime[0:2]))+"30")
                if (int(indavidualTime[2:4]) <= 45):
                    indavidualTimes.append(str(int(indavidualTime[0:2]))+"45")
                
                # This Turns the string of the hour into a list of times inside the hour not including the 1st and last hour
                indavidualTimeRange = range(int(indavidualTime[0:2])+1,int(indavidualTime[5:7]))
                for i in indavidualTimeRange:
                    # This adds all the mins in each hour
                    indavidualTimes.append(str(i)+"00")
                    indavidualTimes.append(str(i)+"15")
                    indavidualTimes.append(str(i)+"30")
                    indavidualTimes.append(str(i)+"45")
                
                # This adds the correct number of mins to the last hour
                if (int(indavidualTime[7:9])) >= 0:
                    indavidualTimes.append(str(int(indavidualTime[5:7]))+"00")
                if (int(indavidualTime[7:9])) >= 15:
                    indavidualTimes.append(str(int(indavidualTime[5:7]))+"15")
                if (int(indavidualTime[7:9])) >= 30:
                    indavidualTimes.append(str(int(indavidualTime[5:7]))+"30")
                if (int(indavidualTime[7:9])) >= 45:
                    indavidualTimes.append(str(int(indavidualTime[5:7]))+"45")
            #This next part puts together the times people are avlaible and puts it on a scale of all times
            allTimes = DateTime.get(date[0])
            for PersonTime in indavidualTimes:
                for ActualTime in allTimes:
                    if ActualTime[0] == PersonTime:
                        ActualTime[1].append(ReplyID[number])

    for TimeNDate in DateTime.items():
        date = TimeNDate[0]
        allTimes = TimeNDate[1]
        for i in range(len(allTimes)-MeetingLen):
            if len(allTimes[i][1]) >= NumRequired:
                people = allTimes[i][1]
                works = True
                peopleavaliable = people.copy()
                for j in range(1,MeetingLen):
                    for person in people:
                        if person not in allTimes[i+j][1]:
                            if person in peopleavaliable:
                                peopleavaliable.remove(person)
                                if len(peopleavaliable) < NumRequired:
                                    works = False
                                    break
                    if not works:
                        break
                
                if works:
                    CombinedTimes = []
                    for j in range(MeetingLen):
                        CombinedTimes.append(allTimes[i+j][0])
                    output.append([date,CombinedTimes,peopleavaliable])
        return output
    


            
            
            






def PushResult():
    """If there is a time where enough people are avaliable this finction will send that information where it needs to go"""
    pass


Examplereply = ["30:0100-0300,1200-1400.31:0800-0900",
                "30:0100-0400.31:0900-1100"]
ExampleLeader = "30:0030-2330.31:0030-2330"
ReplyID = [1001,8008]

bon = CheckOverlap(ExampleLeader,Examplereply,ReplyID,2,8)
for i in bon:
    print(i)




if __name__ == "__main__":
    main()