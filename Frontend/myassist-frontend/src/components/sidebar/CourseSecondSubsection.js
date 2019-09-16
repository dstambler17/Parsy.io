import React, {Component}  from 'react';
import { connect } from 'react-redux'
import CourseItem from './CourseItem'
import {removeSlotSpecial, addSlots} from '../../actions/calActions'
import Exapnd from '../../images/expand-nocircle.png'
import Minus from '../../images/minus-sign-nocircle.png'


class CourseSecondSubsection extends Component {
    
    state = {
        showItems: true,
        isChecked: true
    }

    arraysEqual = (arr1, arr2) => {
        if(arr1.length !== arr2.length)
            return false;
        for(var i = arr1.length; i--;) {
            if(arr1[i] !== arr2[i])
                return false;
        }
    
        return true;
    }
    

    componentWillReceiveProps(nextProps) {
        if (!this.arraysEqual(this.props.isShowing, nextProps.isShowing)){
            //console.log(this.props)
            //console.log(nextProps)
            return
        }
        //console.log(nextProps.checkedParent)
        if (nextProps.checkedParent === false ){
            this.setState({
                isChecked: false
            })
            //Only check if its checked, when unchecking parent
            if (this.refs.section.checked){
                this.refs.section.checked = !this.refs.section.checked;
            }
        } else {
            this.setState({
                isChecked: true
            })
            //Only check if its unchecked, when checking parent
            if (!this.refs.section.checked){
                this.refs.section.checked = !this.refs.section.checked;
            }

        }
        //console.log(this.refs.section)
    
    }
   /* componentDidUpdate(prevProps, prevState){
        if (prevProps.checkedParent !== this.props.checkedParent){
            //console.log("NO MATCH")
            //console.log(prevProps.checkedParent)
            //console.log(this.props.checkedParent)
            if (this.props.checkedParent === false){
                if (this.refs.section.checked){
                    //console.log("I FOUND IT")
                    this.refs.section.checked = !this.refs.section.checked;
                }
            } else {
                if (!this.refs.section.checked){
                    this.refs.section.checked = !this.refs.section.checked;
                }
            }
            
        }
    }

    /*static getDerivedStateFromProps(props, state) {
        //console.log("PASSSS")
        //console.log(props)
        //console.log(state)
        if (props.checkedParent !== state.isChecked) {
          return {
            isChecked: props.checkedParent,
            };
        }
        return null
    } */


    handleCheck = (e) => {
        //Get proper vars to pass in as parameters
        let typeOfMeeting;
        switch(this.props.slotID){
            case 'classmeetingId':
                typeOfMeeting = 'classMeeting'
                break;
            case 'examId':
                typeOfMeeting = 'exam'
                break;
            case 'helpSessionId':
                typeOfMeeting = 'helpSession'
                break;
            case 'assignmentId':
                typeOfMeeting = 'assignment'
                break;
            default:
              break;
          }
        let specialParam = this.props.type
        if (typeOfMeeting === 'helpSession'){
            specialParam = ((this.props.type).includes('Prof')) ? 'Prof' : 'TA'
        }
        let idList = [];
        (this.props.itemList).forEach(function(time) {
            idList.push(time);
        });
        //This says that if box is empty, set false
        //otherwise, set true
        if (!e.target.checked){
            this.props.removeSlotSpecial(this.props.calID, this.props.courseID, this.props.itemList, typeOfMeeting)
            this.setState({
                isChecked: false
            })
        } else {
            this.props.addSlots(this.props.calID, this.props.courseID, '', '', '', typeOfMeeting, '', specialParam)
            this.setState({
                isChecked: true
            })
        }
    }

    handleClick = (e) => {
       if (this.state.showItems){
           this.setState({
                showItems: false
           })
       } else {
            this.setState({
                showItems: true
            })
       }
    }
    
    render () {
        const times = this.props.itemList
        const timeList = (times.length > 0) ? times.map(time => {
            return(
                <div key = {time.id}>
                    <CourseItem time={time.timeItem} id={time.id} location={time.location} sectionType ={time.type} checkedParent={this.state.isChecked} courseID = {this.props.courseID} slotType = {this.props.slotID}/>
                </div>
            )
        }) : (<span></span>)
        const subSectionClass = (this.state.showItems) ? "course-items-style" : "is-display-none course-items-style"
        const plusClass = (!this.state.showItems) ? "" : "is-display-none"
        const minusClass =(this.state.showItems) ? "" : "is-display-none"
        return (
            <div>
                &nbsp;&nbsp;
                <input type="checkbox" name={this.props.type} id = {this.props.type} ref="section" defaultChecked={this.state.isChecked} onChange={this.handleCheck}/>
                <span>{this.props.type}</span>
                <span className="has-margin-left" onClick={this.handleClick}>
                    <img src={Exapnd} className={plusClass} alt="" title="show"/>
                    <img alt="" src={Minus} className={minusClass} title="hide"/>
                </span>
                    <div className={subSectionClass} >
                        {timeList}
                    </div>
                
            </div>
        )
    }
    
}



const mapStateToProps = (state) => {
    return{
        calID: state.calendar.currentCalId
    }
}

const mapDispatchToProps = (dispatch) => {
    return{
        removeSlotSpecial: (calID, courseID, slotIDs, type) => dispatch(removeSlotSpecial(calID, courseID, slotIDs, type)),
        addSlots: (calID, courseID, time, location, subtype, type, slotId, addAll) => dispatch(addSlots(calID, courseID, time, location, subtype, type, slotId, addAll))
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(CourseSecondSubsection)