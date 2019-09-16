import React, { Component} from 'react';
import { connect } from 'react-redux'

class GLogin extends Component {

    componentDidMount(){
        gapi.signin2.render('g-signin2', {
            'scope': 'https://www.googleapis.com/auth/plus.login',
            'width': 200,
            'height': 50,
            'longtitle': true,
            'theme': 'dark',
            'onsuccess': this.onSignIn
          });
    }

    render (){
        return (
            <center><div className="g-signin2" data-onsuccess="onSignIn">Sign In with Google</div></center>
        )
    }
}

export default GLogin
