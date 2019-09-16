import React from 'react';
import { connect } from 'react-redux'
import { showBottomTab, hideBottomTab } from '../../actions/displayActions'
import SideBarContent from './SideBarContent'
import uparrow from '../../images/uparrow.png'

const SideBar = (props) => {
    const handleClick = () => {
        if (props.bottomDisplay){
            props.hideBottomTab()
        } else {
            props.showBottomTab()
        }
    }
    const sideBarClass = (props.bottomDisplay) ? "sidebar sidebar-expanded" : "sidebar"
    const buttonClass = (props.bottomDisplay) ? "expand-btn collapse" : "expand-btn"
    const imageHoverMessage = (props.bottomDisplay) ? "Hide Calendar Manager" : "Display Calendar Manager"
    return (
        <div className={sideBarClass}>
            <div className= {buttonClass} onClick={handleClick} >
                <img src={uparrow} className="tap-up-arrow" title={imageHoverMessage} alt="tap up"/>
            </div>
            <div className="content">
                <h5>My Calendar</h5>
                <SideBarContent />
            </div>
        </div>
    )
}


const mapStateToProps = (state) => {
    return {
        bottomDisplay: state.display.mobileBottomDisplay
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        showBottomTab: () => dispatch(showBottomTab()),
        hideBottomTab: () => dispatch(hideBottomTab())
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(SideBar)
