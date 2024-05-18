from datetime import datetime
#import datetime
def encodeTimes(rawTimes):
    encodedTimes = []
    for item in rawTimes:
        #newTime = None # Null for now since I'm not sure how the datetime is being passed
        newTime = str(item)
        encodedTimes.append(newTime)
        print(type(encodedTimes[0]))
    return encodedTimes

def decodeTimes(dtTimes):
    decodedTimes = []
    for item in dtTimes:
        print(item)
        decodedTime = ""
        decodedTime = datetime.strptime(item, '%d/%m/%y')
        decodedTimes.append(decodedTime)
    return decodedTimes