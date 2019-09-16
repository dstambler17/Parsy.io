import {createEvent, addBackSingleEvent, addBackMultiEvent, addBackAllSingleType} from '../helpers'
const initState = {
    calendars: [],
    currentCalId: null,
    calEvents: [],
    color: 0,
    classColors: [],
    alert: ''
}

const calReducer = (state = initState, action) => {
    switch(action.type){
        case 'CREATE_NEW_CAL':
            const cal = {"id" : action.id, "content" : []}
            //console.log(action.id)
            return{
                ...state,
                calendars: [cal],
                currentCalId: action.id    
            }
        case 'DELETE_CAL':
            return state
        case 'GET_CAL':
            return state
        case 'ADD_CLASS':
            //console.log("adding class")
            let newCal = state.calendars.find(x => x.id === action.calId)
            //console.log(action.result)
            newCal.content = [...newCal.content, action.result]
            let newCals = state.calendars.filter(item => {
                return action.calId !== item.id
            })
            //console.log("NEW CAL START")
            //console.log(newCal)
            //console.log("NEW CAL END")
            //console.log(newCals)
            //console.log("Work now")
            newCals.push(newCal)
            //console.log("NEW CAL AGAIN!!")
            //console.log(newCals)
            let newEvents = createEvent(action.result, state.color)
            let newEventArr = (state.calEvents).concat(newEvents)
            //console.log(newEventArr)
            //console.log("SO MANY LOGS")
            //newEventArr.push(newEvents)

            let addedClassColors = state.classColors
            addedClassColors.push({id: action.result.courseID, color: state.color})
            //console.log("COLORS")
            //console.log(action.result)
            //console.log(addedClassColors)
            let evColor = state.color + 1
            if (evColor > 9){
                evColor = 0
            }
            return {
                ...state,
                calendars: newCals,
                calEvents: newEventArr,
                color: evColor,
                classColors: addedClassColors,
                alert: ''
            }
        case 'ADD_CLASS_ERROR':
            //console.log("YAR I'M A PIRATE")
            const err_status = action.err.status
            //console.log(err_status)
            //return alerts based on error
            let alert;
            if (err_status === 404){
                alert = "Sorry, we don't have that class"
            } else if (err_status === 401){
                alert = "Class already in the calendar"
            } else{
                alert = "Something went wrong"
            }
            //console.log(alert)
            return{
                ...state,
                alert: alert
            } 
        case 'DELETE_CLASS':
            //console.log("Deleting class")
            let modifiedCal = state.calendars.find(x => x.id === action.calId)
            //console.log("modified cal")
            //console.log(modifiedCal.content)
            let lessContent  = modifiedCal.content.filter(item => {
                return item.courseID !== action.courseID
            });
            //console.log("less content")
            //console.log(lessContent)
            modifiedCal.content = lessContent
            let newdelCals = state.calendars.filter(item => {
                return action.calId !== item.id
            })

            newdelCals.push(modifiedCal)
            let trimmedEventList = state.calEvents.filter(event => {
                const eventCourseId = (event.id.split(/\s*[_]\s*/))[0]
                return action.courseID !== eventCourseId
            })
            //Delete class from class color array
            let deletedClassColors = state.classColors.filter(item => {
                return action.courseID !== item.id
            })
            //console.log("COLORS")
            //console.log(deletedClassColors)
            return {
                ...state,
                calendars: newdelCals,
                calEvents: trimmedEventList,
                classColors: deletedClassColors
            }

        case 'DELETE_SLOT_SPECIAL':       
            let specialEventListSlot = state.calEvents.filter(event => {
                const eventSlotId = (event.id.split(/\s*[_]\s*/))[1]
                //console.log(parseInt(eventSlotId))
                return (!(action.slotIDs).includes(parseInt(eventSlotId))) 
            })
            return {
                ...state,
                calEvents: specialEventListSlot 
            }

        case 'DELETE_SLOT':
            let trimmedEventListSlot
            if (action.remove === "yes") {
                let removeType;
                switch(action.slotType){
                    case 'classMeeting':
                        removeType = 'class'
                        break;
                    case 'exam':
                        removeType = 'exam'
                        break;
                    case 'assignment':
                        removeType = 'assignment'
                        break;
                    case 'helpSession':
                        removeType = 'OH'
                        break;
                    default:
                      break;
                  }
                trimmedEventListSlot = state.calEvents.filter(event => {
                    const eventSlots = (event.id.split(/\s*[_]\s*/))
                    const eventCourseID = eventSlots[0].trim()
                    const eventType = eventSlots[2].trim()
                    return (action.courseID.trim() !== eventCourseID || removeType !== eventType)
                })
               
            } else{
                trimmedEventListSlot = state.calEvents.filter(event => {
                    const eventSlotId = (event.id.split(/\s*[_]\s*/))[1]
                    let deleted_Class_edge_boolean;
                    if (eventSlotId === 'undefined') {
                        const eventSlotLoc = (event.id.split(/\s*[_]\s*/))[7]
                        const eventSlotMonth = (event.id.split(/\s*[_]\s*/))[3]
                        const eventSlotDate = (event.id.split(/\s*[_]\s*/))[4]
                        //console.log(event.id)
                        //console.log(parseInt(eventSlotId))
                        //console.log("YAR!!!!!!!!!")
                        //console.log(action.slotID)
                        const splitSlot = (action.slotType === 'assignment' || action.slotType === 'exam') ? 3 : 1
                        const givenStartHour = action.time.split(" ")[splitSlot].split("-")[0].split(":")[0]
                        const givenStartMin = action.time.split(" ")[splitSlot].split("-")[0].split(":")[1]
                        const givenEndHour = action.time.split(" ")[splitSlot].split("-")[1].split(":")[0]
                        const givenEndMinute = action.time.split(" ")[splitSlot].split("-")[1].split(":")[1]
                        const eventStartHours = (event.start.getHours() > 12) ? event.start.getHours() - 12 : event.start.getHours()
                        const eventEndHours = (event.end.getHours() > 12) ? event.end.getHours() - 12 : event.end.getHours()
                        const startMinMatch = (event.start.getMinutes() === 0 && givenStartMin.includes("00")) || (event.start.getMinutes() !== 0 && givenStartMin.includes(event.start.getMinutes().toString()))
                        const endMinMatch = (event.end.getMinutes() === 0 && givenEndMinute.includes("00")) || (event.end.getMinutes() !== 0 && givenEndMinute.includes(event.end.getMinutes().toString()))
                        //console.log("GIVEN INFO BELOW")
                        //console.log(event.start.getDate())
                        const sameDay = event.start.getDate() === parseInt(eventSlotDate) && (event.start.getMonth() + 1) === parseInt(eventSlotMonth)
                        //ACTUALLY FIX THE SOURCE OF THE PROBLEM, the ID BEING UNDEF
                        //console.log("SAME DAY!!!!!!!!!")
                        //console.log(event.start.getDate())
                        //console.log(eventSlotDate)
                        const courseIDhere = (event.id.split(/\s*[_]\s*/))[0]
                        deleted_Class_edge_boolean = sameDay && startMinMatch && endMinMatch && parseInt(givenStartHour) === eventStartHours && parseInt(givenEndHour) === eventEndHours && action.location === eventSlotLoc && courseIDhere === action.courseID//fix edgecase bug
                        //console.log("WOOOOOOOLO")
                        //console.log(deleted_Class_edge_boolean)
                        //console.log(event.start.getDay())
                    } else {
                        deleted_Class_edge_boolean = false
                    }
                    return (action.slotID !== parseInt(eventSlotId) && !deleted_Class_edge_boolean)
                })
                //console.log("I AM CAUGHT HERE!!!!!!!!!!!!!")
            }
            return {
                ...state,
                calEvents: trimmedEventListSlot 
            }
        case 'ADD_SLOT':
            let addType;
            let multiAdd;
            let idName;
            let removeType;
            switch(action.slotType){
                case 'classMeeting':
                    addType = 'class_meeting'
                    multiAdd = true
                    idName = 'classmeetingId'
                    removeType = 'class'
                    break;
                case 'exam':
                    addType = 'exam'
                    multiAdd = false
                    idName = 'examId'
                    removeType = 'exam'
                    break;
                case 'assignment':
                    addType = 'assignment'
                    multiAdd = false
                    idName = 'assignmentId'
                    removeType = 'assignment'
                    break;
                case 'helpSession':
                    addType = 'support'
                    multiAdd = true
                    idName = 'helpSessionId'
                    removeType = 'OH'
                    break;
                default:
                    break;
                }
                let slotModEventsArr;
                let slotModCal = state.calendars.find(x => x.id === action.calID)
                let courseObj = slotModCal.content.find(course => course.courseID === action.courseID)
                let existingSlots;

                //clones object
                let slotModCourse = JSON.parse(JSON.stringify(courseObj))

                const colorObj = state.classColors.find(x=> x.id === action.courseID)
                //console.log("COLOR OBJ")
                //console.log(colorObj)
                
                //These handle all types of adds (section, subsection, item)
                if (action.all === 'yes') {
                    
                    slotModEventsArr = addBackAllSingleType(slotModCourse, colorObj.color, addType, idName)
                    existingSlots = state.calEvents.filter(event => {
                        const eventSlots = (event.id.split(/\s*[_]\s*/))
                        const eventCourseID = eventSlots[0].trim()
                        const eventType = eventSlots[2].trim()
                        return (action.courseID.trim() !== eventCourseID || removeType !== eventType)
                    })

                } else if (action.all === 'Midterm' || action.all === 'Quiz'|| action.all === 'Final' || action.all === 'Lecture' || action.all ==='Section' || action.all ==='Lab' || action.all ==='Homework'){
                    
                    slotModCourse[addType] = slotModCourse[addType].filter(item => {
                        return action.all === item.type
                    })
                    slotModEventsArr = addBackAllSingleType(slotModCourse, colorObj.color, addType, idName)
                    existingSlots = state.calEvents.filter(event => {
                        const eventSlots = (event.id.split(/\s*[_]\s*/))
                        const eventCourseID = eventSlots[0].trim()
                        const subSlotType = eventSlots[5].trim()
                        return (action.courseID.trim() !== eventCourseID || action.all !== subSlotType)
                    })

                } else if (action.all === 'Prof' || action.all === 'TA'){
                    //console.log("IN THE PROF OR TA ZONE")
                    //Because of the way things are named in backend for OH
                    let fixedFilter = (action.all === 'Prof') ? 'Professor Office Hours' : 'TA Office Hours'
                    let newSupport = slotModCourse.support
                    //console.log(newSupport)
                    newSupport = slotModCourse.support.filter(item => {
                        return fixedFilter === item.type
                    })
                    //console.log("HELLO!!!")
                    //console.log(newSupport)
                    slotModCourse.support = newSupport
                    //console.log(slotModCourse.support)
                    //console.log("WHY NO LOG???")
                    slotModEventsArr = addBackAllSingleType(slotModCourse, colorObj.color, addType, idName)
                    existingSlots =  state.calEvents.filter(event => {
                        const eventSlots = (event.id.split(/\s*[_]\s*/))
                        const eventCourseID = eventSlots[0].trim()
                        const subSlotType = eventSlots[5].trim()
                        const professorOrTA = fixedFilter.split(" ")
                        //console.log(professorOrTA[0])
                        return (action.courseID.trim() !== eventCourseID || professorOrTA[0] !== subSlotType)
                    })

                } else {
                    //In this case, we only deal with individual events
                    let slotModItem = slotModCourse[addType].find(x => x[idName] === action.slotId)
                    //console.log("AND NOW GETTING THE SLOT FROM THE PROPER PLACE")
                    //console.log(slotModCourse)
                    //console.log(slotModItem)
                    if (multiAdd){
                        //console.log(colorObj.color)
                        slotModEventsArr = addBackMultiEvent(slotModCourse, slotModItem, colorObj.color, idName, action.time)
                    } else{
                        //console.log(colorObj.color)
                        slotModEventsArr = addBackSingleEvent(slotModCourse, slotModItem, colorObj.color, idName, action.time)
                    }
                    existingSlots = state.calEvents
                }
                    
                const slotAddedRes = (existingSlots).concat(slotModEventsArr)

            return {
                ...state,
                calEvents: slotAddedRes
            }
        case 'SAVE GCAL':
            return state 
        case 'LOAD_CAL':
            const get_cal = {"id" : action.id, "content" : action.result.originalContent}
            //console.log(action.id)
            //console.log(get_cal.content)

            //Regenerates everything on screen
            let stateColor = 0;
            let eventSlotArray = []
            let loadedClassColors = []
            action.result.content.forEach(function(course) {
                //console.log(course)
                eventSlotArray = eventSlotArray.concat(createEvent(course, stateColor))
                loadedClassColors.push({id: course.courseID, color: stateColor})
                stateColor++;
                if (stateColor > 9){
                    stateColor = 0
                }
            });
            //console.log("I HEARBY HAVE AN ELEM")
            //console.log(eventSlotArray)
            return{
                ...state,
                calendars: [get_cal],
                currentCalId: action.id,
                calEvents: eventSlotArray,
                color: stateColor,
                classColors: loadedClassColors,  
            }
            /*
            let newEvents = createEvent(action.result, state.color)
            let newEventArr = (state.calEvents).concat(newEvents)
            //console.log(newEventArr)
            //console.log("SO MANY LOGS")
            //newEventArr.push(newEvents)

            let addedClassColors = state.classColors
            addedClassColors.push({id: action.result.courseID, color: state.color})
            //console.log("COLORS")
            //console.log(action.result)
            //console.log(addedClassColors)
            let evColor = state.color + 1
            if (evColor > 9){
                evColor = 0
            }*/
            
        default:
            return state
    }
}

export default calReducer