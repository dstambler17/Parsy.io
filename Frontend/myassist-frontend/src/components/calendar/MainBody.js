import React, { Component} from 'react';
import { connect } from 'react-redux'
import Header from '../header/Header'
import SideBar from '../sidebar/SideBar'
import { Calendar, Views, Navigate, momentLocalizer } from 'react-big-calendar'
import moment from 'moment'
import { createCal, deleteCal, getCal } from '../../actions/calActions'
import ToolBar from './ToolBar'
import ThreeDayWeek from './ThreeDayWeek'
import { showTimeSlotModal } from '../../actions/modalActions'
import TimeSlotInfoModal from '../modals/TimeSlotInfoModal'
import AboutModal from '../modals/AboutModal'
import SaveModal from '../modals/SaveModal'
import UserLoginModal from '../modals/UserLoginModal'
import {nullSignedInCal, logInReload} from '../../actions/authActions'
import {threeDayWeek, SevenDayWeek} from '../../actions/displayActions'
import * as dates from 'date-arithmetic';
import ReportModal from '../modals/ReportModal';


class MainBody extends Component {

    state = {
        isMobile: null
    }

    
    resize() {
        let currentwindow = (window.innerWidth <= 500);
        if (currentwindow !== this.state.isMobile) {
            this.setState({isMobile: currentwindow});
            //console.log(currentwindow)
            if (currentwindow){
                this.props.threeDayWeek()
            } else {
                this.props.sevenDayWeek()
            }
        }
    }

    componentDidMount() {
        window.addEventListener("resize", this.resize.bind(this));
        this.resize();
        const cookies = this.props.cookies;
        //console.log("COOKERS")
        //console.log(cookies)
        if (cookies.get('id_token') === "null" || cookies.get('id_token') === undefined) {
            if (cookies.get('calID') === "null" || cookies.get('calID') === undefined){
                //console.log("made it")
                this.props.createCal("guest")
            } else{
                //console.log("blin")
                //console.log(cookies.get('calID'))
               const calID = cookies.get('calID')
               this.props.getCal(calID)
            }
        } else{
            //if user is logged in
            if (cookies.get('calID') === "null" || cookies.get('calID') === undefined){
                //console.log("made it")
                this.props.createCal("guest")
                
            } else{
                //console.log("hi")
                //console.log(cookies.get('calID'))
                let calID = cookies.get('calID')
                const id_token = cookies.get('id_token')
                this.props.logInReload(id_token['name'], id_token['picture'], id_token['sub'], id_token, calID)
            }

        }
    }


    render() {

        //Take care of threeday view
        ThreeDayWeek.range = date => {
            let start = date
            let end = dates.add(start, 2, 'day')
          
            let current = start
            let range = []
          
            while (dates.lte(current, end, 'day')) {
              range.push(current)
              current = dates.add(current, 1, 'day')
            }
          
            return range
          }
          
          ThreeDayWeek.navigate = (date, action) => {
            switch (action) {
              case Navigate.PREVIOUS:
                return dates.add(date, -3, 'day')
          
              case Navigate.NEXT:
                return dates.add(date, 3, 'day')
          
              default:
                return date
            }
          }

          ThreeDayWeek.title = date => {
            return `My threeday week: ${date.toLocaleDateString()}`
          }

        //Set cookies if null
        const cookies = this.props.cookies;
        if (cookies.get('calID') === "null" || cookies.get('calID') === undefined){
            //If user logged in then refreshed, get calid
            if (cookies.get('id_token') !== "null" && cookies.get('id_token') !== undefined){
                let calID = this.props.currentCalID
                const id_token = cookies.get('id_token')
                this.props.logInReload(id_token['name'], id_token['picture'], id_token['sub'], id_token, calID)
                cookies.set('calID', this.props.currentCalID, { path: '/' })
            }
            cookies.set('calID', this.props.currentCalID, { path: '/' })
        }

        //Get Cal if user logs in
        if (this.props.signedincalID !== null && this.props.user !== null){
            this.props.getCal(this.props.signedincalID)
            this.props.nullSignedInCal()
        }

        //Once the user logs in set cookie to id_token
        if (this.props.id_token !== null && (cookies.get('id_token') === "null" || cookies.get('id_token') === undefined)){
            //console.log("Hi!!!")
            cookies.set('id_token', this.props.id_token, { path: '/' })
        }

        
        const eventStyleGetter = function (event, start, end, isSelected, color) {
            //console.log(event.id);
            var backgroundColor = event.color;
            var style = {
                backgroundColor: backgroundColor,
                borderRadius: '0px',
                opacity: 0.8,
                fontsize: '10px',
                color: 'black',
                border: '0px',
                display: 'block'
            };
            return {
                style: style
            };
        }
        const weekView = (this.state.isMobile) ? ThreeDayWeek : true //get three day view if mobile, week otherwise
        const localizer = momentLocalizer(moment)
        var today = new Date();
        const dd = today.getDate()
        const mm = today.getMonth()
        const yyyy = today.getFullYear();
        return (
            <div>
                <div>
                    <Header cookies={this.props.cookies} />
                    <div className="main-content">
                        <SideBar />
                        <div className="calender-wrapper">
                            <Calendar
                                popup
                                localizer={localizer}
                                events={this.props.calEvents}
                                onNavigate={() => { }}
                                views={{month: true, week: weekView, day: true}}
                                defaultView={Views.WEEK}
                                min={new Date(2019, 10, 0, 6, 0, 0)}
                                max={new Date(2019, 10, 0, 20, 0, 0)}
                                showMultiDayTimes
                                onSelectEvent={event => this.props.showTimeModal(event.id, event.start, event.end)}
                                scrollToTime={new Date(2018, 1, 1, 6)}
                                defaultDate={new Date(yyyy, mm, dd)}
                                eventPropGetter={(eventStyleGetter)}
                                components={{
                                    toolbar: ToolBar
                                }}
                            />
                            <span className = "is-small-footer-text">
                                 &copy; Parsy.io 2019 
                            </span>
                        </div>
                    </div>
                </div>
                <TimeSlotInfoModal />
                <AboutModal/>
                <UserLoginModal cookies={this.props.cookies}/>
            </div>
        )
    }
}


const mapStateToProps = (state, ownProps) => {
    //console.log(state)
    return {
        user: state.auth.user,
        calendar: state.calendar.calendars,
        currentCalID: state.calendar.currentCalId,
        calEvents: state.calendar.calEvents,
        signedincalID: state.auth.signedincalID,
        id_token: state.auth.id_token,
        cookies: ownProps.cookies
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        createCal: (user) => dispatch(createCal(user)),
        deleteCal: (id) => dispatchEvent(deleteCal(id)),
        showTimeModal: (title, start, end) => dispatch(showTimeSlotModal(title, start, end)),
        getCal: (id) => dispatch(getCal(id)),
        logInReload: (username, picture, userid, id_token, calID) => dispatch(logInReload(username, picture, userid, id_token, calID)),
        nullSignedInCal: () => dispatch(nullSignedInCal()),
        threeDayWeek: () => dispatch(threeDayWeek()),
        sevenDayWeek: () => dispatch(SevenDayWeek())
    }
}


export default connect(mapStateToProps, mapDispatchToProps)(MainBody)