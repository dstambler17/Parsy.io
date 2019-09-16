import {baseurl} from '../constants.js'

export const createCal = (user) => (dispatch) => {
    const body = { "username" : user}
    fetch(baseurl + "course/newCal", {
		method: 'POST', // or 'PUT'
		body: JSON.stringify(body), // data can be `string` or {object}!
		headers:{
			'Content-Type': 'application/json'
		}
	}).then(res => res.json())
	.then(response => {
    let id = response['id']
    return dispatch({
        type: "CREATE_NEW_CAL",
        user: user,
        id: id
      })
  }).catch(error => console.error('Error:', error));
}

export const getCal = (calid) => (dispatch) => {
  fetch(baseurl + 'course/' + calid, {
    method: 'GET'
  }).then(res => res.json()).then(response => {
    return dispatch({
      type: "LOAD_CAL",
      id: calid,
      result: response
    })
}).catch(error => console.error('Error', error))
 
}

export const deleteCal = (id) => (dispatch) => {
    fetch(baseurl + 'course/' + id, {
         method: 'DELETE',
    }).then(response => {
    dispatch({
        type: "DELETE_CAL",
        id: id
    })
    })
    .catch(error => console.error('Error:', error));
}

const fetchHandler = (res) => {
  if (res.status >= 400 && res.status < 600) {
    return Promise.reject(res);
  }
  return res.json();
}

export const addCourseToCal = (courseID, id) => (dispatch) => {
    let url = baseurl + "course/" + id + "/addClassHelp/" + courseID + 'Fall 2019'
    //console.log(url)
    fetch(url, {
		method: 'POST', // or 'PUT'
	}).then(fetchHandler, error => {
    //network error
    dispatch({ type: 'ADD_CLASS_ERROR', err: error})})
	.then(response => {
    return dispatch({
        type: "ADD_CLASS",
        calId: id,
        result: response
      })
  }).catch(error => {return dispatch({
    type: "ADD_CLASS_ERROR",
    err: error
    })
  });
}

export const deleteCourse = (courseID, calId) => (dispatch) => {
  let url = baseurl + 'course/' + calId + '/removeClass/' + courseID
  //console.log(url)
  fetch(url, {
    method: 'DELETE',
  }).then(response => {
    dispatch({
      type: "DELETE_CLASS",
      courseID: courseID,
      calId: calId
  })
  }).catch(error => console.error('Error:', error));
}

export const saveToGCal = (calID, userid) => (dispatch) => {
  let url = baseurl + 'course/saveCal/' + calID
  let data = {'userid' : userid}
  fetch(url, {
		method: 'POST', // or 'PUT'
		body: JSON.stringify(data), // data can be `string` or {object}!
		headers:{
			'Content-Type': 'application/json'
		}
  }).then(res => {
 dispatch({
  type: "SAVE_GCAL"
 })
  }).catch(error => console.error('Error:', error))
}

export const removeSlotSpecial = (calID, courseID, slotIDs, type) => (dispatch) => {
  let deleteType
  //For the URL
  switch(type){
    case 'classMeeting':
      deleteType = 'deleteClassMeeting'
      break;
    case 'exam':
      deleteType = 'deleteExam'
      break;
    case 'assignment':
      deleteType = 'deleteAssignment'
      break;
    case 'helpSession':
      deleteType = 'deleteOH'
      break;
    default:
      break;
  }
  let url = baseurl + type + '/' + deleteType + '/' + calID + '/' + courseID
  let content = [];
  let ids = [];
  //console.log("BELOW ARE SLOT IDS")
  //console.log(slotIDs)
  slotIDs.forEach(function(idElem) {
    content.push({'time' : idElem.timeItem, "location" : idElem.location, "type" : idElem.type})
    ids.push(idElem.id)
  });
//console.log(content)
  const info = {"content": content, "all": "no"}
  //console.log(url)
  //console.log(JSON.stringify(info))
  fetch(url, {
		method: 'DELETE', 
    body: JSON.stringify(info),
    headers: {'Content-Type': 'application/json'}
	}).then(res => {
    dispatch({
      type: "DELETE_SLOT_SPECIAL",
      courseID: courseID,
      slotType: type,
      slotIDs: ids
    })
  })
	.catch(error => console.error('Error:', error));
}

export const removeSlot = (calID, courseID, slotID, time, location, subtype, type, removeAll) => (dispatch) => {
  let deleteType
  //For the URL
  switch(type){
    case 'classMeeting':
      deleteType = 'deleteClassMeeting'
      break;
    case 'exam':
      deleteType = 'deleteExam'
      break;
    case 'assignment':
      deleteType = 'deleteAssignment'
      break;
    case 'helpSession':
      deleteType = 'deleteOH'
      break;
    default:
      break;
  }
  let url = baseurl + type + '/' + deleteType + '/' + calID + '/' + courseID
  const info = {"content": [{"time" : time, "location" : location, "type" : subtype}], "all": removeAll}
  //console.log(url)
  //console.log(JSON.stringify(info))
  fetch(url, {
		method: 'DELETE', 
    body: JSON.stringify(info),
    headers: {'Content-Type': 'application/json'}
	}).then(res => {
    dispatch({
      type: "DELETE_SLOT",
      courseID: courseID,
      remove: removeAll,
      slotType: type,
      slotID: slotID,
      time: time,
      location: location
    })
  })
	.catch(error => console.error('Error:', error));
}


export const addSlots = (calID, courseID, time, location, subtype, type, slotId, addAll) => (dispatch) => {
  let addType;
  let timeType;
  let restoreType;
  //For the URL
  switch(type){
    case 'classMeeting':
        addType = 'addClassMeeting'
        timeType= "times"
        restoreType = "restoreClassMeeting"
      break;
    case 'exam':
        addType = 'addExam'
        timeType= "datetime"
        restoreType = "restoreExam"
      break;
    case 'assignment':
        addType = 'addAssignment'
        timeType= "datetime"
        restoreType = "restoreAssignment"
      break;
    case 'helpSession':
        addType = 'addOH'
        timeType= "time"
        restoreType = "restoreOH"
      break;
    default:
      break;
  }
  let urlCenter = (addAll === "yes") ? restoreType : addType
  let url = baseurl + type + '/' + urlCenter + '/' + calID + '/' + courseID
  let info = {"content": [{[timeType]: time, "location" : location, "type": subtype}], "all": addAll}
  //console.log("THIS IS THE URL INFO")
  //console.log(url)
  //console.log(JSON.stringify(info))
  fetch(url, {
		method: 'POST', 
    body: JSON.stringify(info),
    headers: {'Content-Type': 'application/json'}
	}).then(res => {
    dispatch({
      type: "ADD_SLOT",
      courseID: courseID,
      slotType: type,
      calID: calID,
      slotId: slotId,
      time: time,
      all: addAll
    })
  })
	.catch(error => console.error('Error:', error));
}
