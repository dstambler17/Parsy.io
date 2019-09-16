import React, {useRef, useEffect} from 'react'
import {connect} from 'react-redux'
import {closeSaveModal} from '../../actions/modalActions'
import GoogleCalCheck from '../../images/GoogleCalCheck.jpg'


const SaveModal = (props) => {
  const saveMod = useRef();

  const handleClick = e => {
    if (saveMod.current.contains(e.target)) {
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

    const showHideClassName = props.show ? "modal display-block" : "modal display-none";
   return (
    <div id="my-modal"  className={showHideClassName}>
    <div ref={saveMod} className="modal-content">
      <div>
        <span> <button className=" close is-black" onClick={props.closeModal}>&times;</button></span>
        <center><h2 className="is-size-3">Success!</h2></center>
      </div>
      <div className="modal-body">
        <div className="center-text">Calendar Successfully exported to Google Calendar</div>
        <div className="center-text"><img alt="" src={GoogleCalCheck} className="googleCal-Image-Small"/></div>
      </div>
    </div>
  </div>
  );
}

const mapStateToProps = (state) => {
    return{
        show: state.modal.showSaveCalModal
    }
}

const mapDispatchToProps = (dispatch) => {
    return{
        closeModal: () => dispatch(closeSaveModal()),
    }
}



export default connect(mapStateToProps, mapDispatchToProps)(SaveModal)