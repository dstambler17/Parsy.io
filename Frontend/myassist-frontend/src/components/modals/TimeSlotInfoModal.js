import React, {useRef, useEffect} from 'react'
import {connect} from 'react-redux'
import {closeTimeSlotModal} from '../../actions/modalActions'
import {deleteCourse} from '../../actions/calActions'
import {removeSlot} from '../../actions/calActions'

const TimeSlotInfoModal = (props) => {
  const timeMod = useRef();

  const handleClick = e => {
    if (timeMod.current.contains(e.target)) {
      //console.log(e.target)
      //console.log(props.title)
      //console.log("YEAHAHHAHA")
      //console.log(props.start)
      //console.log(props.end)
      return;
    }
    // outside click 
    props.closeModal()
  };
  
  useEffect(() => {
      // add when mounted
      document.addEventListener("mousedown", handleClick);
      // return function to be called when unmounted
      return () => {
        document.removeEventListener("mousedown", handleClick);
      };
    });

    const showHideClassName = props.show ? "modal display-block" : "modal display-none";

    const handleDelete = () => {
        const courseId = (props.title.split(/\s*[_]\s*/))[0]
        //console.log(courseId)
        props.deleteCourse(courseId, props.calID)
        props.closeModal()
    }

    //Converts datetime object back to string
    const handleTime = (time) => {
      const stringTime = (time !== null) ? time.toString() : ''
      if (stringTime === '') {
        return ''
      }
      const timeChunks = stringTime.split(" ")
      const date = timeChunks[0] + " " + timeChunks[1] + " " + timeChunks[2] + " " +timeChunks[3]
      const timeOfDay = (timeChunks[4].trim()).split(":")
      const AmPm = (parseInt(timeOfDay[0]) >= 12) ? "pm" : "am"
      const hour = (parseInt(timeOfDay[0]) > 12) ? parseInt(timeOfDay[0]) - 12 : parseInt(timeOfDay[0])
      const cleanedTime = hour.toString() + ":" + timeOfDay[1] + AmPm
      return (date + " " +cleanedTime)
    }

    const slot_info = (props.title !== null) ? props.title.split(/\s*[_]\s*/) : ['', '', '', '', '', '', '', '', '', '', '', '']
    const header_text_end = (slot_info[2] === "OH") ? "Office Hours" : ''
    const header_text = slot_info[6] + " " + slot_info[5] + " " + header_text_end
    const location = slot_info[7]
    let courseIDAlone;

    if (slot_info[0].includes("Spring 20")){
      courseIDAlone = (slot_info[0].split("Spring 20"))[0]
    } else if (slot_info[0].includes("Fall 20")) {
      courseIDAlone = (slot_info[0].split("Fall 20"))[0]
    } else{
      courseIDAlone = ''
    }
    
    const endTime = handleTime(props.end)
    const startTime = handleTime(props.start)
    const eventType = (slot_info[5] === "Professor") ? slot_info[8] : slot_info[5]
    const event = eventType + " " + header_text_end
    

   return (
    <div id="my-modal" className={showHideClassName}>
    <div ref={timeMod}className="modal-content">
      <div className="modal-header">
        <span> <button className="negate-button close" onClick={props.closeModal}>&times;</button></span>
        <h3 className="is-size-4 modal-title">{header_text}</h3>
      </div>
      <div className="modal-body">
        <b>Event:</b> {event} <br/>
        <b>Course ID:</b> {courseIDAlone} <br/>
        <b>Location:</b> {location} <br/>
        <b>Start:</b> {startTime}<br/>
        <b>End:</b> {endTime}<br/>
      </div>
      <div className="modal-footer">
	      <button type="button" className="btn is-delete" id ="delete" onClick={handleDelete}>Delete Course</button>
      </div>
    </div>
  </div>
  );
}

const mapStateToProps = (state) => {
    return{
        show: state.modal.showtimeSlotModal,
        title: state.modal.timeSlotModalTitle,
        start: state.modal.timeSlotstartTime,
        end: state.modal.timeSlotendTime,
        calID: state.calendar.currentCalId
    }
}

const mapDispatchToProps = (dispatch) => {
    return{
        closeModal: () => dispatch(closeTimeSlotModal()),
        deleteCourse: (courseID, calId) => dispatch(deleteCourse(courseID, calId)),
        removeSlot: (calID, courseID, slotID, time, location, subtype, type, removeAll) => dispatch(removeSlot(calID, courseID, slotID, time, location, subtype, type, removeAll)),

    }
}



export default connect(mapStateToProps, mapDispatchToProps)(TimeSlotInfoModal)