import React from 'react'
import {connect} from 'react-redux'
import {showLogInSignUpModal} from '../../actions/modalActions'
import Nav from 'react-bootstrap/Nav'

const SignedOutLinks = (props) => {
    const handleClick = () => {
        props.showLogInSignUpModal()
    }
    return (
        <div>
            <Nav.Link onClick={handleClick}>Login</Nav.Link>
        </div>
    )
}

const mapDispatchToProps = (dispatch) => {
    return {
        showLogInSignUpModal: () => dispatch(showLogInSignUpModal())
    }
  }

export default connect(null, mapDispatchToProps)(SignedOutLinks)