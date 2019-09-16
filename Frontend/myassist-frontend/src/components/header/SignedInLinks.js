import React from 'react'
import {connect} from 'react-redux'
import Nav from 'react-bootstrap/Nav'
import Avatar from 'react-avatar';
import Dropdown from 'react-bootstrap/Dropdown'
import {logOut} from '../../actions/authActions'
import {getCal, createCal} from '../../actions/calActions'

//import { GoogleLogout } from 'react-google-login';

const SignedInLinks = (props) => {
    const handleClick = () => {
        var auth2 = window.gapi.auth2.getAuthInstance();
            auth2.signOut().then(function () {
            //console.log('User signed out.');
        });
        props.logOut()
        
        //Cookie setting when logging out
        const cookies = props.cookies
        if (cookies.get('calID') !== undefined){
            //console.log(cookies.get('calID'))
            props.getCal(cookies.get('calID'))
        } else{
            props.createCal("guest")
        }
        
        //console.log("LOGOUT COOKIES")
        cookies.set('id_token', "null", { path: '/' })
        //console.log(cookies)
    }
    return (
        <div>
            
            <Dropdown className="avatar-items">
            <Avatar size="40"  src={props.profile} round={true}/>
            <Dropdown.Toggle split variant="" className="is-clear" id="dropdown-split-basic" />
                  <Dropdown.Menu className="dropdown-shifted-right">
                    <Dropdown.Item href="" onClick={handleClick} eventKey='logout'>Logout</Dropdown.Item>
                  </Dropdown.Menu>
            </Dropdown>
            <span className="sign-out-link">
                <Nav.Link onClick={handleClick} className="small-right-margin">Logout</Nav.Link>
                <Avatar size="40"  src={props.profile} round={true}/>
            </span>
        </div>
    )
}

const mapStateToProps = (state) => {
    return {
        username: state.auth.user,
        profile: state.auth.profilePic,
        id_token: state.auth.id_token,
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        logOut: () => dispatch(logOut()),
        getCal: (calid) => dispatch(getCal(calid)),
        createCal: (user) => dispatch(createCal(user))
    }
  }
export default connect(mapStateToProps, mapDispatchToProps)(SignedInLinks)