import React, {Component} from 'react';
import { connect } from 'react-redux'
import CourseSubsection from './CourseSubsection'
import {removeSlot, addSlots, deleteCourse} from '../../actions/calActions'
import Exapnd from '../../images/expand-nocircle.png'
import Minus from '../../images/minus-sign-nocircle.png'

class Course extends Component { 
    
    state = {
        showOH: false,
        showClass: false,
        showExams: false,
        showAssignments: false,
        isCheckedOH: true,
        isCheckedExam: true,
        isCheckedClassMeeting: true,
        isCheckedAssignment: true
    }

    deleteCourse = (e) => {
        this.props.deleteCourse(this.props.id, this.props.calID)
    }
    
    handleClick = (e) => {
        const boolType = e.target.id
        //console.log("BOOLTYPE!!!")
        //console.log(e.target)
       if (this.state[boolType]){
           this.setState({
                [e.target.id]: false
           })
       } else {
        this.setState({
            [e.target.id]: true
        })
       }
    }

    handleCheck = (e) => {
        //This says that if box is empty, set false
        //otherwise, set true
        let typeofData;
            switch(e.target.id){
                case 'isCheckedOH':
                    typeofData = 'helpSession'
                    break;
                case 'isCheckedExam':
                    typeofData = 'exam'
                    break;
                case 'isCheckedClassMeeting':
                    typeofData = 'classMeeting'
                    break;
                case 'isCheckedAssignment':
                    typeofData = 'assignment'
                    break;
                default:
                    break;
            }
        if (!e.target.checked){
            
            this.props.removeSlot(this.props.calID, this.props.id, '', '', '', '', typeofData, "yes")
            this.setState({
                [e.target.id]: false
            })
        } else {
            this.props.addSlots(this.props.calID, this.props.id, '', '', '', typeofData, '', 'yes')
            this.setState({
                [e.target.id]: true
            })
        }
    }

    

    render () {
        const OH_Display = (this.state.showOH) ? "" : "is-display-none"
        const classMeeting_Display = (this.state.showClass) ? "" : "is-display-none"
        const exam_Display = (this.state.showExams) ? "" : "is-display-none"
        const assignment_Display = (this.state.showAssignments) ? "" : "is-display-none"
        const displayList = [OH_Display, classMeeting_Display, exam_Display, assignment_Display]

        const plusClass_OH = (!this.state.showOH) ? "" : "is-display-none"
        const plusClass_classtime = (!this.state.showClass) ? "" : "is-display-none"
        const plusClass_exam = (!this.state.showExams) ? "" : "is-display-none"
        const plusClass_assignment = (!this.state.showAssignments) ? "" : "is-display-none"

        const this_course_id = this.props.id
        const cicleColor = this.props.classColors.find(x=> x.id === this_course_id);
        const color_Arr = ['#3ff939', '#3abefc', '#fc1631', '#e6f957', '#0945f7', '#ed9421', '#13efd2', '#d6c7b3', '#2c9904', '#991219'];
        //console.log("COLOR IS BEING PRINTED OUT")
        //console.log(cicleColor.color)
        const circle_background_color = {'color' : color_Arr[cicleColor.color]};
        return (
            <div>
            <span className="circle" style={circle_background_color}></span>
            <b>{this.props.title}&nbsp;&nbsp;</b><span className="sidebar-delete-course" onClick={this.deleteCourse} title="Delete Course">&times;</span>
                <div>
                    <input type="checkbox" name={this.props.id} isshowing={this.state.showOH} id = "isCheckedOH" defaultChecked={this.state.isCheckedOH} onChange={this.handleCheck}/>
                    <span id="showOH">Office Hours</span>
                    <span onClick={this.handleClick} className="has-margin-left">
                        <img id="showOH" src={Exapnd} className={plusClass_OH} alt="" title="exapnd"/>
                        <img  id="showOH" alt="" src={Minus} className={OH_Display} title="hide"/>
                    </span><br/>
                    <div className= {OH_Display}>
                        <CourseSubsection items={this.props.officeHours} eventType="repeat" slotid="helpSessionId" courseID = {this.props.id} checkedParent={this.state.isCheckedOH} isShowing={displayList} />
                    </div>  
                </div>
                <div>
                    <input type="checkbox" name={this.props.id} isshowing={this.state.showClass} id = "isCheckedClassMeeting" defaultChecked={this.state.isCheckedClassMeeting} onChange={this.handleCheck}/>
                    <span id="showClass"> Class Times</span>
                    <span className="has-margin-left" onClick={this.handleClick}>
                        <img id="showClass" src={Exapnd} className={plusClass_classtime} alt="" title="expand"/>
                        <img id="showClass" alt="" src={Minus} className={classMeeting_Display} title="hide"/>
                    </span><br/>
                    <div className= {classMeeting_Display}>
                        <CourseSubsection items={this.props.classMeetings} eventType="repeat" slotid="classmeetingId" courseID = {this.props.id} checkedParent={this.state.isCheckedClassMeeting} isShowing={displayList}/>
                    </div>
                </div>
                <div>
                    <input type="checkbox" name={this.props.id} isshowing={this.state.showExams} id = "isCheckedExam" defaultChecked={this.state.isCheckedExam} onChange={this.handleCheck} />
                    <span id="showExams" >Exams</span>
                    <span  className="has-margin-left" onClick={this.handleClick}>
                        <img id="showExams" src={Exapnd} className={plusClass_exam} alt="" title="expand"/>
                        <img id="showExams" alt="" src={Minus} className={exam_Display} title="hide"/>
                    </span><br/>

                    <div className= {exam_Display}>
                        <CourseSubsection items={this.props.exams} eventType="one time" slotid="examId" courseID = {this.props.id} checkedParent={this.state.isCheckedExam} isShowing={displayList}/>
                    </div>
                </div>

                <div>
                    <input type="checkbox" name={this.props.id} isshowing={this.state.showAssignments} id = "isCheckedAssignment" defaultChecked={this.state.isCheckedAssignment} onChange={this.handleCheck} />
                    <span id="showAssignments" >Assignments</span>
                    <span  className="has-margin-left" onClick={this.handleClick}>
                        <img id="showAssignments" src={Exapnd} className={plusClass_assignment} alt="" title="expand"/>
                        <img id="showAssignments" alt="" src={Minus} className={assignment_Display} title="hide"/>
                    </span><br/>

                    <div className= {assignment_Display}>
                        <CourseSubsection items={this.props.assignments} eventType="one time" slotid="assignmentId" courseID = {this.props.id} checkedParent={this.state.isCheckedAssignment} isShowing={displayList}/>
                    </div>
                </div>
            </div>
        )
    }
}

const mapStateToProps = (state) => {
    return{
        calID: state.calendar.currentCalId,
        classColors: state.calendar.classColors
    }
}

const mapDispatchToProps = (dispatch) => {
    return{
        removeSlot: (calID, courseID, slotID, time, location, subtype, type, removeAll) => dispatch(removeSlot(calID, courseID, slotID, time, location, subtype, type, removeAll)),
        addSlots: (calID, courseID, time, location, subtype, type, slotId, addAll) => dispatch(addSlots(calID, courseID, time, location, subtype, type, slotId, addAll)),
        deleteCourse: (courseID, calId) => dispatch(deleteCourse(courseID, calId))
    }
}


export default connect(mapStateToProps, mapDispatchToProps)(Course)