import React, {useRef, useEffect} from 'react'
import {connect} from 'react-redux'
import {closeHowToModal} from '../../actions/modalActions'

const HowToUseModal = (props) => {
   const howToMod = useRef();

  const handleClick = e => {
      if (howToMod.current.contains(e.target)) {
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
     <div id="my-modal" className={showHideClassName}>
    <div ref={howToMod} className="modal-content">
      <div className="modal-header">
        <span> <button className="negate-button close" onClick={props.closeModal}>&times;</button></span>
        <center><h2 className="is-size-3">How to use Parsy</h2></center>
      </div>
      <div className="modal-body">
        <p>Step 1...</p>
      </div>
      <div className="modal-footer">
        <button type="button" className="btn btn-secondary" onClick={props.closeModal}>Close</button>
      </div>
    </div>
  </div>
  );
}

const mapStateToProps = (state) => {
    return{
        show: state.modal.showHowToModal
    }
}

const mapDispatchToProps = (dispatch) => {
    return{
        closeModal: () => dispatch(closeHowToModal()),
    }
}



export default connect(mapStateToProps, mapDispatchToProps)(HowToUseModal)