from datetime import datetime
#import datetime
def encodeTimes(rawTimes):
    encodedTimes = []
    for item in rawTimes:
        #newTime = None # Null for now since I'm not sure how the datetime is being passed
        newTime = str(item)
        encodedTimes.append(newTime)
    return encodedTimes

def decodeTimes(dtTimes):
    decodedTimes = []
    for item in dtTimes:
        decodedTime = ""
        decodedTime = datetime.strptime(item, '%d/%m/%y')
        decodedTimes.append(decodedTime)
    return decodedTimes