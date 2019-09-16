import React, {useRef, useEffect} from 'react'
import {connect} from 'react-redux'
import {closeAboutModal} from '../../actions/modalActions'

const AboutModal = (props) => {
  const AboutMod = useRef();

  const handleClick = e => {
      if (AboutMod.current.contains(e.target)) {
        //console.log(e.target)
        return;
      }
      // outside click 
      props.closeModal()
  };
  
  useEffect(() => {
      // add when mounted
      document.addEventListener("mousedown", handleClick);
      //call when unmounted
      return () => {
        document.removeEventListener("mousedown", handleClick);
      };
    });

    const showHideClassName = props.show ? "modal display-block" : "modal display-none";
   
   return (
     <div id="my-modal" className={showHideClassName}>
    <div ref={AboutMod} className="modal-content">
      <div className="modal-header about-modal-header">
        <span className="center-content"><h2 className="is-size-3">About Parsy</h2></span>
      </div>
      <div className="modal-body">
						Hey there! We're a small team of JHU alumni and students, and we develop technical solutions that make life better for students by simplifying the most tedious processes
            of your college career. Each semester, we were stuck reading through syllabi and scheduling all of our assignments,
            midterms, and office hours on a week by week basis. We've all had homework deadlines sneak up on us,
            and have gotten blindsided by exams and we figured - why not automate the entire process? 
            Parsy takes your syllabi and automatically schedules all of your assignments, exams, office
            hours and more for you throughout the entire year in an easy to read and easy to customize calendar.
            One click and you're done! 
            In addition we will soon be launching
            our parsing on demand tool; if we don't have your class available already,
            you can submit the syllabi for it on the spot, and Parsy will automatically schedule it just
            like it would if it were in our database. Furthermore, it will be added to our database so that everyone else can use it as well.
            But in the meantime feel free to test out our app for the select classes that we currently have in our database. 
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
        show: state.modal.showAboutModal
    }
}

const mapDispatchToProps = (dispatch) => {
    return{
        closeModal: () => dispatch(closeAboutModal()),
    }
}



export default connect(mapStateToProps, mapDispatchToProps)(AboutModal)