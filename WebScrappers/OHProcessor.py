
''' Helper for removing spaces between lines'''
def clearSpaces(wordlist):
    for x in range(len(wordlist)):
        if wordlist[x] == '-' and x +1 < len(wordlist) and x > 0:
            wordlist[x] = wordlist[x-1] + "-" + wordlist[x + 1]
    return wordlist

'''Help to add days in week'''
def addWeekDay(inputWord):
    weekdayList = ["monday", "tuesday", "wednesday", "thursday", "friday", \
    "saturday", "sunday", "mondays", "tuesdays", "wednesdays", "thursdays", "fridays", \
    "saturdays", "sundays", \
    "su", "m", "tu", "w", "th", "f", "sa", "sun", \
    "tue", "tues", "th", "thu", "thur", "thurs", "sat", "mon", "wed", "fri"]
    if inputWord.lower() in weekdayList:
        return inputWord

def cleanItem(time):
    checkList = time.split("-")
    endSymbol = ""
    if ("am" in checkList[0] or "pm" in checkList[0]) and ("am" in checkList[1] or "pm" in checkList[1]):
        return time
    count = 0
    for x in checkList:
        if "am" in x:
            endSymbol = "am"
            checkList[count] =  x.replace(endSymbol, "")
        if "pm" in x:
            endSymbol = "pm"
            checkList[count] = x.replace("pm", "")
        count = count + 1
    return (checkList[0] + endSymbol + "-" + checkList[1] + endSymbol)

'''Helper to find and add the right times'''
def addTimes(item):
    if "-" in item and ("am" in item or "pm" in item):
        item = cleanItem(item)
        return item

    times = item.split("-")
    properTimes = 0
    resTimes = []
    if len(times) != 2:
        return None
    for x in times:
        if ":" in x:
            hourMins = x.split(":")
            if hourMins[0].isdigit() and hourMins[1].isdigit():
                properTimes = int(hourMins[0])
        elif x.isdigit():
            properTimes = x

        if properTimes != 0:
            timeOfDay = "pm" if int(properTimes) < 8 or int(properTimes) == 12 else "am"
            s1 = x + timeOfDay
            resTimes.append(s1)
        else:
            return None
    return (resTimes[0] + "-" + resTimes[1])

def addColonZeros(time):
    res = time.split("-")
    track = 0
    for x in res:
        if ":" not in x:
            res[track] = x.replace("pm", ":00pm") if ("pm" in x) else x.replace("am", ":00am")
        track = track + 1
    return (res[0] + "-" + res[1])


def processString(input):
    daysInWeek = []
    weekTimes = []

    negativeSymbols = [',', '\\', '/', ')', '(', '.']
    for symb in negativeSymbols:
        input = input.replace(symb, " ")
    wordlist = input.split(" ")
    wordlist = clearSpaces(wordlist)
    puncList = ['.', "\'", ';', ':', '\"', ',', '/', ')', '(']
    for item in wordlist:
        if len(item) == 0:
            continue
        if item[len(item) - 1] in puncList:
            item = item[:-1]

        day = addWeekDay(item)
        if day != None:
            daysInWeek.append(day)
        time = addTimes(item)
        if time != None:
            time = addColonZeros(time)
            weekTimes.append(time)
            while len(daysInWeek) > len(weekTimes):
                weekTimes.append(time)
        if len(weekTimes) > len(daysInWeek) and len(daysInWeek) != 0:
            daysInWeek.append(daysInWeek[len(daysInWeek) - 1])

    final_result = ""
    if len(daysInWeek) == len(weekTimes):

        for i in range(len(daysInWeek)):
            final_result = final_result + daysInWeek[i] + " " + weekTimes[i] + ", "

    #print(final_result)
    return final_result
