import React, {Component}  from 'react';
import { connect } from 'react-redux'
import {removeSlot, addSlots} from '../../actions/calActions'

class CourseItem extends Component {
    state = {
        isChecked: true
    }
    handleChange = (e) => {
        //This says that if box is empty, set false
        //otherwise, set true
        let typeOfMeeting;
        switch(this.props.slotType){
            case 'classmeetingId':
                typeOfMeeting = 'classMeeting'
                break;
            case 'examId':
                typeOfMeeting = 'exam'
                break;
            case 'assignmentId':
                typeOfMeeting = 'assignment'
                break;
            case 'helpSessionId':
                typeOfMeeting = 'helpSession'
                break;
            default:
              break;
          }
        if (!e.target.checked){
            this.props.removeSlot(this.props.calID, this.props.courseID, this.props.id, this.props.time, this.props.location, this.props.sectionType, typeOfMeeting, "no")
            this.setState({
                isChecked: false
            })

        } else {
            this.props.addSlots(this.props.calID, this.props.courseID, this.props.time, this.props.location, this.props.sectionType, typeOfMeeting, this.props.id, 'no')
            this.setState({
                isChecked: true
            })
        }
    }

    componentDidUpdate(prevProps, prevState){
        //console.log("WHAT IS WHY WORK I UPDATED YOUUUUU??")
        //console.log(prevProps.checkedParent)
        //console.log(this.props.checkedParent)
        if (prevProps.checkedParent !== this.props.checkedParent){
            //console.log("NO MATCH")
            //console.log(prevProps.checkedParent)
            //console.log(this.props.checkedParent)
            if (this.props.checkedParent === false){
                if (this.refs.item.checked){
                    //console.log("I FOUND IT")
                    this.refs.item.checked = !this.refs.item.checked;
                }
            } else if (this.props.checkedParent === true) {
                if (!this.refs.item.checked){
                    this.refs.item.checked = !this.refs.item.checked;
                }
            }
            
        }
    }

    static getDerivedStateFromProps(props, state) {
        //console.log(props)
        //console.log(state)
        if (props.checkedParent !== state.isChecked) {
          return {
            isChecked: props.checkedParent,
            };
        }
        return null
    }

    componentDidMount (){
        //This is to uncheck the boxes on page reload if they have been
        //unchecked
        //console.log("THE COMPONENT HAS MOUNTED")
        //console.log(this.props.id)
        const filteredSlots = this.props.calSlots.filter(event => {
            const eventSlotId = (event.id.split(/\s*[_]\s*/))[1]
            return this.props.id === parseInt(eventSlotId)
        })
        if (filteredSlots.length === 0){
            //this.setState({
            //    isChecked: false
            //})
            this.refs.item.checked = !this.refs.item.checked
        }
    }

    render () {
        let input = (this.props.time).trim();
        let daytimearray = [input.substr(0,input.indexOf(' ')), input.substr(input.indexOf(' ')+1) ];
        
        let weekDay;
            if(daytimearray[0].toLowerCase().startsWith("su")){      weekDay = "Su"}
            else if(daytimearray[0].toLowerCase().startsWith("m")){  weekDay = "M"}
            else if(daytimearray[0].toLowerCase().startsWith("tu")){ weekDay = "Tu"}
            else if(daytimearray[0].toLowerCase().startsWith("w")){  weekDay = "W"}
            else if(daytimearray[0].toLowerCase().startsWith("th")){ weekDay = "Th"}
            else if(daytimearray[0].toLowerCase().startsWith("f")){  weekDay = "F"}
            else if(daytimearray[0].toLowerCase().startsWith("sa")){ weekDay = "Sa"}
        
        
        const timeSlot = (this.props.sectionType === 'Homework' || this.props.type === 'Final' || this.props.type === 'Midterm' || this.props.type === 'Quiz') ? input  : weekDay + " " + daytimearray[1]
        //console.log(this.props.sectionType)
        return (
            <div>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <input type="checkbox" name={timeSlot} id={this.props.id} ref="item" defaultChecked={this.state.isChecked} onChange={this.handleChange} />{timeSlot}
            </div>
        )
    }
    
}

const mapStateToProps = (state) => {
    return{
        calID: state.calendar.currentCalId,
        calSlots: state.calendar.calEvents
    }
}

const mapDispatchToProps = (dispatch) => {
    return{
        removeSlot: (calID, courseID, slotID, time, location, subtype, type, removeAll) => dispatch(removeSlot(calID, courseID, slotID, time, location, subtype, type, removeAll)),
        addSlots: (calID, courseID, time, location, subtype, type, slotId, addAll) => dispatch(addSlots(calID, courseID, time, location, subtype, type, slotId, addAll))
    }
}



export default connect(mapStateToProps, mapDispatchToProps)(CourseItem)