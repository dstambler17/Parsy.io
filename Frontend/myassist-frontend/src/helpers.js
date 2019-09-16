//Used to restore a class back to the time table
export const addBackMultiEvent = (result, section, colorIndx, idName, time) => {
    const colors = ['#3ff939', '#3abefc', '#fc1631', '#e6f957', '#0945f7', '#ed9421', '#13efd2', '#d6c7b3', '#2c9904', '#991219'];
    let start_month;
    const end_month = 11;
    let start_date;
    const end_date = 6;
    if (idName === "helpSessionId"){
        start_month = 8
        start_date = 8
    } else  {
        start_month = 7
        start_date = 25
    }
    const last_day_per_month = {0: 31, 1: 29, 2: 31, 3: 30, 4: 31, 5: 30, 6: 31, 7: 31, 8: 30, 9: 31, 10: 30, 11: 31}
    let repeatEvents = []
    if(time.trim().toString() === ""){
        return;
    }
    let stringinput = time.trim().toString();
    let daytimearray = [stringinput.substr(0,stringinput.indexOf(' ')), stringinput.substr(stringinput.indexOf(' ')+1) ];
    
    let date;
    if(daytimearray[0].toLowerCase().startsWith("su")){      date = 0}
    else if(daytimearray[0].toLowerCase().startsWith("m")){  date = 1}
    else if(daytimearray[0].toLowerCase().startsWith("tu")){ date = 2}
    else if(daytimearray[0].toLowerCase().startsWith("w")){  date = 3}
    else if(daytimearray[0].toLowerCase().startsWith("th")){ date = 4}
    else if(daytimearray[0].toLowerCase().startsWith("f")){  date = 5}
    else if(daytimearray[0].toLowerCase().startsWith("sa")){ date = 6}

    let times = daytimearray[1].split(/\s*[-]\s*/);
    let startTime = times[0].split(/\s*[:]\s*/);
    let endTime = times[1].split(/\s*[:]\s*/);

    let startTimeHour = parseInt(startTime[0]);
    let startTimeMin = parseInt(startTime[startTime.length-1].toLowerCase().replace('am','').replace('pm',''))
    if(startTime[startTime.length-1].toLowerCase().includes("pm") || (endTime[endTime.length-1].toLowerCase().includes("pm") && !startTime[startTime.length-1].toLowerCase().includes("am"))){
        startTimeHour = parseInt(startTime[0])%12 + 12;
    }

    let endTimeHour = parseInt(endTime[0]);
    let endTimeMin = parseInt(endTime[endTime.length-1].toLowerCase().replace('am','').replace('pm',''))
    if(endTime[endTime.length-1].toLowerCase().includes("pm") && !endTime[0].toLowerCase().includes("12")){
        endTimeHour = parseInt(endTime[0])%12 + 12;
    }

    //Add events for every week of the semester
    let month_counter = start_month
    let day_counter = start_date
    const slotType = (idName === "helpSessionId") ? "_OH" : "_class"
    const slotTypeTitle = (idName === "helpSessionId") ? section['type'].split(" ")[0] + " Office Hour " : section['type'].split(" ")[0] 
    while (month_counter < end_month  || day_counter <= end_date) {
        //Check that the semester actually began
        if (month_counter === 7 && date+day_counter < 29){
            day_counter = 7 - (last_day_per_month[month_counter] - day_counter)
            month_counter = month_counter + 1
            continue
        }

        let event={id: result['courseID'] + '_' + section[idName] + slotType + '_' + (month_counter + 1).toString() + '_' + (day_counter +date).toString() + '_' + section['type'].split(" ")[0] + '_'+ result['courseName'] + '_' + section['location'] + '_' + result['professor'],
            title:  result['courseName'] + " " + slotTypeTitle,
            start:  new Date(2019, month_counter, date+day_counter, startTimeHour, startTimeMin),
            end: new Date(2019, month_counter, date+day_counter, endTimeHour, endTimeMin),
            color: colors[colorIndx]
        }
        if (day_counter + 7 > last_day_per_month[month_counter]){
            day_counter = 7 - (last_day_per_month[month_counter] - day_counter)
            month_counter = month_counter + 1
        } else {
            day_counter = day_counter + 7
        }
        
        repeatEvents.push(event)
    }
        
    return repeatEvents
}


export const addBackSingleEvent = (result, section, colorIndx, idName, time) => {
    const colors = ['#3ff939', '#3abefc', '#fc1631', '#e6f957', '#0945f7', '#ed9421', '#13efd2', '#d6c7b3', '#2c9904', '#991219'];
    let singleEvents = []
        //console.log(section)
        //console.log(time)
        if(time.trim().toString() === ""){
            return;
        }
        let stringinput = time.trim().toString();
         let daytimearray = stringinput.split(" ")
         //console.log(daytimearray)

        let month;
        if(daytimearray[0].toLowerCase().startsWith("jan")){      month = 0}
        else if(daytimearray[0].toLowerCase().startsWith("feb")){  month = 1}
        else if(daytimearray[0].toLowerCase().startsWith("mar")){ month = 2}
        else if(daytimearray[0].toLowerCase().startsWith("apr")){  month = 3}
        else if(daytimearray[0].toLowerCase().startsWith("may")){ month = 4}
        else if(daytimearray[0].toLowerCase().startsWith("jun")){  month = 5}
        else if(daytimearray[0].toLowerCase().startsWith("jul")){ month = 6}
        else if(daytimearray[0].toLowerCase().startsWith("aug")){ month = 7}
        else if(daytimearray[0].toLowerCase().startsWith("sep")){ month = 8}
        else if(daytimearray[0].toLowerCase().startsWith("oct")){ month = 9}
        else if(daytimearray[0].toLowerCase().startsWith("nov")){ month = 10}
        else if(daytimearray[0].toLowerCase().startsWith("dec")){ month = 11}

        let date = parseInt(daytimearray[1])
        //console.log("BELOW ARE TIMES")
        //console.log(month)
        //console.log(daytimearray[1])
        let times = daytimearray[2].split(/\s*[-]\s*/);
        let startTime = times[0].split(/\s*[:]\s*/);
        let endTime = times[1].split(/\s*[:]\s*/);

        let startTimeHour = parseInt(startTime[0]);
        let startTimeMin = parseInt(startTime[startTime.length-1].toLowerCase().replace('am','').replace('pm',''))
        if(startTime[startTime.length-1].toLowerCase().includes("pm") || (endTime[endTime.length-1].toLowerCase().includes("pm") && !startTime[startTime.length-1].toLowerCase().includes("am"))){
            startTimeHour = parseInt(startTime[0])%12 + 12;
        }

        let endTimeHour = parseInt(endTime[0]);
        let endTimeMin = parseInt(endTime[endTime.length-1].toLowerCase().replace('am','').replace('pm',''))
        if(endTime[endTime.length-1].toLowerCase().includes("pm") && !endTime[0].toLowerCase().includes("12")){
            endTimeHour = parseInt(endTime[0])%12 + 12;
        }

        //Add events for every week of the semester
        const slotType = (idName === "examId") ? "_exam" : "_assignment" 
        let event={id: result['courseID'] + '_' +  section[idName]  + slotType + '_' + (month + 1).toString() + '_' + (date).toString() + '_' + section['type'].split(" ")[0] + '_' + result['courseName'] + '_' + section['location'] + '_' + result['professor'],
            title:  result['courseName'] + " " + section['type'].split(" ")[0],
            start:  new Date(2019, month, date, startTimeHour, startTimeMin),
            end: new Date(2019, month, date, endTimeHour, endTimeMin),
            color: colors[colorIndx]
        }
        singleEvents.push(event)
        
    return singleEvents

}




//----------------------------------------------------------------------------------------------------------------
const oneTimeEventsAdder = (result, colors, colorIndex, singleItemType, idType) => {
    let singleEvents = []
    for (let i = 0; i < result[singleItemType].length; i++){
        const section = result[singleItemType][i]
        //console.log(section)
        const time = section['datetime']
        //console.log(time)
        if(time.trim().toString() === ""){
            return;
        }
        let stringinput = time.trim().toString();
         let daytimearray = stringinput.split(" ")
         //console.log(daytimearray)

        let month;
        if(daytimearray[0].toLowerCase().startsWith("jan")){      month = 0}
        else if(daytimearray[0].toLowerCase().startsWith("feb")){  month = 1}
        else if(daytimearray[0].toLowerCase().startsWith("mar")){ month = 2}
        else if(daytimearray[0].toLowerCase().startsWith("apr")){  month = 3}
        else if(daytimearray[0].toLowerCase().startsWith("may")){ month = 4}
        else if(daytimearray[0].toLowerCase().startsWith("jun")){  month = 5}
        else if(daytimearray[0].toLowerCase().startsWith("jul")){ month = 6}
        else if(daytimearray[0].toLowerCase().startsWith("aug")){ month = 7}
        else if(daytimearray[0].toLowerCase().startsWith("sep")){ month = 8}
        else if(daytimearray[0].toLowerCase().startsWith("oct")){ month = 9}
        else if(daytimearray[0].toLowerCase().startsWith("nov")){ month = 10}
        else if(daytimearray[0].toLowerCase().startsWith("dec")){ month = 11}

        let date = parseInt(daytimearray[1])
        //console.log("BELOW ARE TIMES")
        //console.log(month)
        //console.log(daytimearray[1])
        let times = daytimearray[2].split(/\s*[-]\s*/);
        let startTime = times[0].split(/\s*[:]\s*/);
        let endTime = times[1].split(/\s*[:]\s*/);

        let startTimeHour = parseInt(startTime[0]);
        let startTimeMin = parseInt(startTime[startTime.length-1].toLowerCase().replace('am','').replace('pm',''))
        if(startTime[startTime.length-1].toLowerCase().includes("pm") || (endTime[endTime.length-1].toLowerCase().includes("pm") && !startTime[startTime.length-1].toLowerCase().includes("am"))){
            startTimeHour = parseInt(startTime[0])%12 + 12;
        }

        let endTimeHour = parseInt(endTime[0]);
        let endTimeMin = parseInt(endTime[endTime.length-1].toLowerCase().replace('am','').replace('pm',''))
        if(endTime[endTime.length-1].toLowerCase().includes("pm") && !endTime[0].toLowerCase().includes("12")){
            endTimeHour = parseInt(endTime[0])%12 + 12;
        }
        //let text = document.createTextNode(daytimearray[1] + ' ' + section['type'] + ': ' + section['location']);

        //Add events for every week of the semester
        const slotType = (singleItemType === "exam") ? "_exam" : "_assignment"
        let event={id: result['courseID'] + '_' +  section[idType]  + slotType + '_' + (month + 1).toString() + '_' + (date).toString() + '_' + section['type'].split(" ")[0] + '_'+ result['courseName'] + '_' + section['location'] + '_' + result['professor'],
            title:  result['courseName'] +  " " + section['type'].split(" ")[0],
            start:  new Date(2019, month, date, startTimeHour, startTimeMin),
            end: new Date(2019, month, date, endTimeHour, endTimeMin),
            color: colors[colorIndex]
        }
        singleEvents.push(event)
        
    }
    return singleEvents

}


const repeatEventsAdder = (result, colors, colorIndex, repeatItemType, idType) => {
    //The if below is to find the start date for class or OH, we will assume
    //that OHs do not begin on the first day of class
    let start_month;
    const end_month = 11;
    let start_date;
    const end_date = 6;
    if (repeatItemType === "support"){
        start_month = 8
        start_date = 8
    } else  {
        start_month = 7
        start_date = 25
    }
    const last_day_per_month = {0: 31, 1: 29, 2: 31, 3: 30, 4: 31, 5: 30, 6: 31, 7: 31, 8: 30, 9: 31, 10: 30, 11: 31}
    let repeatEvents = []
    for (let i = 0; i < result[repeatItemType].length; i++){
        const section = result[repeatItemType][i]
        const time = section['times']
        if(time.trim().toString() === ""){
            return;
        }
        let stringinput = time.trim().toString();
        let daytimearray = [stringinput.substr(0,stringinput.indexOf(' ')), stringinput.substr(stringinput.indexOf(' ')+1) ];
        
        let date;
        if(daytimearray[0].toLowerCase().startsWith("su")){      date = 0}
        else if(daytimearray[0].toLowerCase().startsWith("m")){  date = 1}
        else if(daytimearray[0].toLowerCase().startsWith("tu")){ date = 2}
        else if(daytimearray[0].toLowerCase().startsWith("w")){  date = 3}
        else if(daytimearray[0].toLowerCase().startsWith("th")){ date = 4}
        else if(daytimearray[0].toLowerCase().startsWith("f")){  date = 5}
        else if(daytimearray[0].toLowerCase().startsWith("sa")){ date = 6}

        let times = daytimearray[1].split(/\s*[-]\s*/);
        let startTime = times[0].split(/\s*[:]\s*/);
        let endTime = times[1].split(/\s*[:]\s*/);

        let startTimeHour = parseInt(startTime[0]);
        let startTimeMin = parseInt(startTime[startTime.length-1].toLowerCase().replace('am','').replace('pm',''))
        if(startTime[startTime.length-1].toLowerCase().includes("pm") || (endTime[endTime.length-1].toLowerCase().includes("pm") && !startTime[startTime.length-1].toLowerCase().includes("am"))){
            startTimeHour = parseInt(startTime[0])%12 + 12;
        }

        let endTimeHour = parseInt(endTime[0]);
        let endTimeMin = parseInt(endTime[endTime.length-1].toLowerCase().replace('am','').replace('pm',''))
        if(endTime[endTime.length-1].toLowerCase().includes("pm") && !endTime[0].toLowerCase().includes("12")){
            endTimeHour = parseInt(endTime[0])%12 + 12;
        }
        //let text = document.createTextNode(daytimearray[1] + ' ' + section['type'] + ': ' + section['location']);

        //Add events for every week of the semester
        let month_counter = start_month
        let day_counter = start_date
        const slotType = (repeatItemType === "support") ? "_OH" : "_class"
        const slotTypeTitle = (repeatItemType === "support") ? section['type'].split(" ")[0] + " Office Hour " : section['type'].split(" ")[0] 
        while (month_counter < end_month  || day_counter <= end_date) {
            //Check that the semester actually began
            if (month_counter === 7 && date+day_counter < 29){
                day_counter = 7 - (last_day_per_month[month_counter] - day_counter)
                month_counter = month_counter + 1
                continue
            }

            let event={id: result['courseID'] + '_' + section[idType] + slotType + '_' + (month_counter + 1).toString() + '_' + (day_counter +date).toString() + '_' + section['type'].split(" ")[0] + '_'+ result['courseName'] + '_' + section['location'] + '_' + result['professor'], 
                title:  result['courseName'] + " " + slotTypeTitle,
                start:  new Date(2019, month_counter, date+day_counter, startTimeHour, startTimeMin),
                end: new Date(2019, month_counter, date+day_counter, endTimeHour, endTimeMin),
                color: colors[colorIndex]
            }
            if (day_counter + 7 > last_day_per_month[month_counter]){
                day_counter = 7 - (last_day_per_month[month_counter] - day_counter)
                month_counter = month_counter + 1
            } else {
                day_counter = day_counter + 7
            }
            
            repeatEvents.push(event)
        }
        
    }
    return repeatEvents

}

export const addBackAllSingleType = (result, colorIndex, type, typeId ) => {
    const colors = ['#3ff939', '#3abefc', '#fc1631', '#e6f957', '#0945f7', '#ed9421', '#13efd2', '#d6c7b3', '#2c9904', '#991219'];
    let events;
    if (type === 'exam' || type === 'assignment'){
        events = oneTimeEventsAdder(result, colors, colorIndex, type, typeId)
    } else {
        events = repeatEventsAdder(result, colors, colorIndex, type, typeId)
    }
    return events
}

export const createEvent = (result, colorIndex) => {
    const colors = ['#3ff939', '#3abefc', '#fc1631', '#e6f957', '#0945f7', '#ed9421', '#13efd2', '#d6c7b3', '#2c9904', '#991219'];
    
    let events = repeatEventsAdder(result, colors, colorIndex, 'support', 'helpSessionId')
    const ClassEvents = repeatEventsAdder(result, colors, colorIndex, 'class_meeting', 'classmeetingId')
    
    const examEvents = oneTimeEventsAdder(result, colors, colorIndex, 'exam', 'examId')
    const assignmentEvents = oneTimeEventsAdder(result, colors, colorIndex, 'assignment', 'assignmentId')
    events = events.concat(ClassEvents)
    events = events.concat(examEvents)
    events = events.concat(assignmentEvents)
    //console.log("BELOW ARE WITH EXAM EVENTS")
    //console.log(examEvents)
    return events         
}
