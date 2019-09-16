import React, {Component}  from 'react';
//import { connect } from 'react-redux'
import CourseSecondSubsection from './CourseSecondSubsection'

/** The point of this file is to break down
 * The JSON for parts of a class into subsections.
 * So for example, from office hours, we want, prof OH, TA OH
 * And learning den times. While from exam, we want midterm, final etc.
*/
class CourseSubsection extends Component {    
    
    render () {

        const getItemsIntoSection = (items, eventType, slotid) => {
            const slot = (eventType === "repeat") ? "times" : "datetime"
            const sections = {}
            items.forEach(function(item) {
                const type = item.type
                if (sections[type] === undefined){
                    sections[type] = [{timeItem: item[slot], id: item[slotid], location: item.location, type: item.type}]
                } else{
                    sections[type].push({timeItem: item[slot], id: item[slotid], location: item.location, type: item.type})
                }
              });
              return sections
        }

       const {items, eventType, courseID, slotid, checkedParent, isShowing} = this.props;
       //console.log("IS SHOWING!!!!!!!!!!!!!!!!!!!!!!")
       //console.log(isShowing)
       const sections = getItemsIntoSection(items, eventType, slotid)
       const keys = Object.keys(sections)
       const subSections = (keys.length > 0) ? keys.map(individualKey => {
            const list = sections[individualKey]
            return(
                <div key = {individualKey}>
                    <CourseSecondSubsection type = {individualKey} itemList={list} courseID = {courseID} checkedParent = {checkedParent} slotID = {slotid} isShowing={isShowing}/>
                </div>
            )
        }) : (<span></span>)

        //const sectionClass = (this.props.isshowing) ? "" : "is-display-none"
        return (
            <div className="course-subsection-style">
                {subSections}
            </div>
        )
    }
    
}
export default CourseSubsection