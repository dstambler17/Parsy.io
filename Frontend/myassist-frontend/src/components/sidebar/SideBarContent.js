import React, { Component} from 'react';
import { connect } from 'react-redux'
import Course from './Course'


class SideBarContent extends Component {
    
    render (){
    
        const {calendars, currentCalId} = this.props;
        const calendar =  calendars.find(x => x.id === currentCalId)
        const courses = (calendars.length > 0) ? ( (calendars[0].content.length > 0) ? calendar['content'].map(course => {
            return(
                <div key = {course.courseID} className="course-slot">
                    <Course title={course.courseName} id= {course.courseID} officeHours={course.support} prof={course.professor} assignments = {course.assignment} exams = {course.exam} classMeetings = {course.class_meeting}/>
                </div>
            )
        }) : (<p>Add some courses</p>)): (<p></p>)

        //For each course add to props,
        //Pass them in as Course Items
        //For each item,
       return (
        <div className="sideBar-course-content">
            {courses}
       </div>
       ); 
    }
}

const mapStateToProps = (state) => {
    return {
        calendars: state.calendar.calendars,
        currentCalId: state.calendar.currentCalId
    }
}


export default connect(mapStateToProps, null)(SideBarContent)