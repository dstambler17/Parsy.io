import React, {useRef, useEffect} from 'react'
import {connect} from 'react-redux'
import {closeLogInSignUpModal} from '../../actions/modalActions'
import GoogleLogin from 'react-google-login';
import {logIn} from '../../actions/authActions'


const UserLoginModal = (props) => {
  const signInMod = useRef();

  const handleClick = e => {
    if (signInMod.current.contains(e.target)) {
      //console.log(e.target)
      return;
    }
    // outside click 
    props.closeModal()
  };
  


  useEffect(() => { 


      // add when mounted
      document.addEventListener("mousedown", handleClick);
      // return function to be called when unmounted
      return () => {
        document.removeEventListener("mousedown", handleClick);
      };
    });

    const onSignIn = (googleUser) => {
        //console.log("WHA!!!!!!!!!")
        //console.log(googleUser.code)
        props.logIn(googleUser.code, props.currentcalID)
        props.closeModal()
        
        //Cookie setting when logging in
        /*const cookies = props.cookies
        //console.log("LOGIN COOKIES")
        cookies.set('name', profile.getName(), { path: '/' })
        cookies.set('urlImage', profile.getImageUrl(), { path: '/' })
        cookies.set('token', id_token, { path: '/'})
        //console.log(cookies)*/

    }

    const showHideClassName = props.show ? "modal display-block" : "modal display-none";
   return (
    <div id="my-modal"  className={showHideClassName}>
    <div ref={signInMod} className="modal-content">
      <div>
        <span> <button className=" close is-black" onClick={props.closeModal}>&times;</button></span>
        <center><h2 className="is-size-3">Sign In</h2></center>
      </div>
      <div className="modal-body">
        <div className="center-text">Sign in to keep your calendar preserved</div>
        <br/>
        <center><GoogleLogin
            clientId="528707814554-sahtu1f07gvbs8sksjol3dgmjcg45h1e.apps.googleusercontent.com"
            buttonText="Login with Google"
            onSuccess={onSignIn}
            cookiePolicy={'single_host_origin'}
            accessType="offline"
            responseType="code"
            scopes="profile email https://www.googleapis.com/auth/calendar.events"
        /></center>
      </div>
    </div>
  </div>
  );
}

const mapStateToProps = (state) => {
    return{
        show: state.modal.showLoginSignUpModal,
        currentcalID: state.calendar.currentCalId,
        signedincalID: state.auth.signedincalID
    }
}

const mapDispatchToProps = (dispatch) => {
    return{
        closeModal: () => dispatch(closeLogInSignUpModal()),
        logIn: (creds, calid) => dispatch(logIn(creds, calid)),
    }
}



export default connect(mapStateToProps, mapDispatchToProps)(UserLoginModal)