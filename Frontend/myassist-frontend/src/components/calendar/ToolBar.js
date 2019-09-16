import React from 'react';
import moment from 'moment'
import {connect} from 'react-redux'
import {saveToGCal} from '../../actions/calActions'
import {showSaveModal} from '../../actions/modalActions'


const ToolBar = (toolbar) => {
    const goToBack = () => {
        if (toolbar.view === "week"){
            const minusDays =  (toolbar.threeDayWeek) ? 3 : 7
            let newDate = new Date(
                    toolbar.date.getFullYear(),
                    toolbar.date.getMonth(),
                    toolbar.date.getDate() - minusDays,
                    1
                );
                toolbar.onNavigate('prev', newDate);
            }
        else if (toolbar.view === "month"){
            toolbar.date.setMonth(toolbar.date.getMonth() - 1);
            toolbar.onNavigate('prev');
        } else { //for day view
            let newDate = new Date(
                toolbar.date.getFullYear(),
                toolbar.date.getMonth(),
                toolbar.date.getDate() - 1,
                1
            );
            toolbar.onNavigate('prev', newDate);
        }
      
    };
  
    const goToNext = () => {
        if (toolbar.view === "week"){
            const plusDays =  (toolbar.threeDayWeek) ? 3 : 7
            //console.log(toolbar.view)
           let newDate = new Date(
                toolbar.date.getFullYear(),
                toolbar.date.getMonth(),
                toolbar.date.getDate() + plusDays,
                1
            );
            toolbar.onNavigate('next', newDate);
        } else if (toolbar.view === "month"){
            toolbar.date.setMonth(toolbar.date.getMonth() + 1);
            toolbar.onNavigate('next');
        } else { //Incase of DayView
            let newDate = new Date(
                toolbar.date.getFullYear(),
                toolbar.date.getMonth(),
                toolbar.date.getDate() + 1,
                1
            );
            toolbar.onNavigate('next', newDate);
        }
      
    };
  
    const goToCurrent = () => {
        if (toolbar.view === "week"){
            const now = new Date();
            toolbar.onNavigate('current', now);
        } else if (toolbar.view === "month") {
            const now = new Date();
            toolbar.date.setMonth(now.getMonth());
            toolbar.date.setYear(now.getFullYear());
            toolbar.onNavigate('current'); 
        } else { //Incase of Day view
            const now = new Date();
            toolbar.onNavigate('current', now); 
        }
      
    };

    /** const goToMonth = () => {
        toolbar.onView('month')
    }

    const goToWeek = () => {
        toolbar.onView('week')
    } */

    const changeView = (e) => {
        let value = e.target.value
        if (value === 'week'){
            toolbar.onView('week')
        } else if (value === 'month'){
            toolbar.onView('month')
        } else { //dayview
            toolbar.onView('day')
        }
    }
    
    const handleGCalSave = () => {
        if (toolbar.id_token !== null) {
            toolbar.saveToGCal(toolbar.currentCalID, toolbar.id_token['sub'])
            toolbar.showSaveModal()
        }
    }

    const label = () => {
      const month_abbreviation_mapper = {"January" : "Jan", "February" : "Feb", "March" : "Mar", "April" : "Apr", "May" : "May",
        "June" : "Jun", "July" : "Jul", "August" : "Aug", "September" : "Sep", "October" : "Oct", "November" : "Nov", "December" : "Dec"}
      const date = moment(toolbar.date);
      const responsive_label = (toolbar.threeDayWeek) ? month_abbreviation_mapper[date.format('MMMM')] : date.format('MMMM')
      return (
        <span><b>{responsive_label}</b><span> {date.format('YYYY')}</span></span>
      );
    };
 
    const weekName = (toolbar.threeDayWeek) ? "3-day" : "Week" 
    return (
      <div>
        <span align="left" className="is-inline-flex">
          <button className = "toolbar-button" onClick={goToCurrent}>Today</button>
          <button className = "toolbar-leftright" onClick={goToBack}>&#8249;</button>
          <button className = "toolbar-leftright" onClick={goToNext}>&#8250;</button>
          <label className ="toolbar-label">{label()}</label>

        </span>
        <span className="toolbar-right-items is-inline-flex">
            <select className="toolbar-dropdown" onChange={changeView} value={toolbar.view}>
                <option value="day">Day</option>
                <option value="week">{weekName}</option>
                <option value="month">Month</option>
            </select>

        </span>
      </div>
    );
  };

const mapStateToProps = (state) => {
    return {
        currentCalID: state.calendar.currentCalId,
        id_token: state.auth.id_token,
        threeDayWeek: state.display.threeDayWeek
    }
}

const mapDispatchToProps = (dispatch) => {
  return {
    saveToGCal : (calID, userid) => dispatch(saveToGCal(calID, userid)),
    showSaveModal: () => dispatch(showSaveModal())
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(ToolBar)