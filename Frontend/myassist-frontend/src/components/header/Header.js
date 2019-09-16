import React from 'react'
import ParsyFull from '../../images/ParsyioLogo.png'
import { connect } from 'react-redux'
import ParsyMobile from '../../images/ParsyioCalendarOnlyLogo.png'
import SignedOutLinks from './SignedOutLinks'
import SignedInLinks from './SignedInLinks'
import AddClass from './AddClass'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import {showAboutModal, showHowToModal, showReportModal} from '../../actions/modalActions'

const Header = (props) => {
    const rightLinks = (props.isSignedIn) ? <SignedInLinks cookies={props.cookies} /> : <SignedOutLinks />
    return (
       <Navbar bg="primary" expand="lg" variant="dark" className="grayscale">
            <Navbar.Brand href="/">
            <img alt="" src={ParsyFull} width="200" height="50" className=" is-logo is-full-size-logo"/>
            <img alt="" src={ParsyMobile} width="50" height="50" className="is-logo is-mobile-logo"/>
            </Navbar.Brand>
            <Nav><AddClass/></Nav>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="mr-auto">
                </Nav>
                <Nav>
                    <Nav.Link onClick = {props.showAboutModal} title="About Us">About</Nav.Link>
                    <Nav.Link href="https://docs.google.com/forms/d/e/1FAIpQLSffT_-v-M-FULYNPvJYC3tmpI0jsg4OaH0j2eRlGGqW3QRk3g/viewform" title="Report Bugs or Issues">Report</Nav.Link>
                    {rightLinks}   
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    )
}

const mapStateToProps = (state) => {
    return {
        isSignedIn: state.auth.isSignedIn
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        showAboutModal: () => dispatch(showAboutModal()),
        showReportModal: () => dispatch(showReportModal()),
        showHowToModal: () => dispatch(showHowToModal()),
    }
}


export default connect(mapStateToProps, mapDispatchToProps)(Header)