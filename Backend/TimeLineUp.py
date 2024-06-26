def CheckOverlap(IdAvaliability,MembersNeeded,hoursneeded):
    #The following piece of code makes a list of all times split into 15 min incraments
    Times = []
    for hour in range(0,24):
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
    

    for i in range(len(Times)-hoursneeded*4):
        works = True
        if len(Times[i][1]) >= MembersNeeded:
            members = Times[i][1].copy()
            for j in range(1,hoursneeded*4+1):
                    for member in members:
                        if member not in Times[i+j][1]:
                            members.remove(member)
                    if len(members) < MembersNeeded:
                        works = False
            if works:
                if len(str(Times[i][0])) != 4:
                    Times[i][0] = "0" + Times[i][0]
                return [Times[i][0],members]
    return []


print()

[[1, '01:00:00', '07:30:00'],]
2
2