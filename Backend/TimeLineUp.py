def CheckOverlap(IdAvaliability,MembersNeeded,hoursneeded):
    #The following piece of code makes a list of all times split into 15 min incraments
    Times = []
    Times.append(["0000",[]])
    Times.append(["0015",[]])
    Times.append(["0030",[]])
    Times.append(["0045",[]])
    for hour in range(1,24):
        for min in ["00","15","30","45"]:
            Times.append([(str(hour) + min),[]])

    for user in IdAvaliability:
        AvaliabilityStart = user[1]
        AvaliabilityEnd = user[2]
        AvaliabilityStart = AvaliabilityStart.split(":")[0:2]
        AvaliabilityStart = "".join(AvaliabilityStart)
        AvaliabilityEnd = AvaliabilityEnd.split(":")[0:2]
        AvaliabilityEnd = "".join(AvaliabilityEnd)
        for time in Times:
            if int(time[0]) >= int(AvaliabilityStart) and int(time[0]) <= int(AvaliabilityEnd):
                time[1].append(user[0])
    
    output = []
    for i in range(len(Times)-hoursneeded*4):
        works = True
        if len(Times[i][1]) >= MembersNeeded:
            for j in range(1,hoursneeded*4+1):
                if not(len(Times[i+j][1]) >= MembersNeeded):
                    works = False
            if works:
                output.append([Times[i]])
    return output


print(CheckOverlap([[1,"18:00:00.00000","21:45:00.000000"],[2,"00:15:00.000000","22:30:00.000000"]],2,2))