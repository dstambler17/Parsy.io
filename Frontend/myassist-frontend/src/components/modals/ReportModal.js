import React, {Component} from 'react'
import {connect} from 'react-redux'
import {baseurl} from '../../constants.js'
import {closeReportModal} from '../../actions/modalActions'
import {addCourseToCal} from '../../actions/calActions'
import axios from 'axios';
import loader from '../../images/loader.gif'
import Alert from 'react-bootstrap/Alert'
import Suggestions from '../header/Suggestions'

class ReportModal extends Component {

    state = {
        input: '',
        courselinkInput: '',
        loading: false,
        success: false,
        failure: false,
        alertMessage: '',
        showSuggestions: false,
        cursor: 0,
        courseSearches: []
    }

    ref = React.createRef();

    handleKeyDown = (e) => {
    
        const submitActive = (id) => {
          this.setState({
            input: id,
            showSuggestions: false
          })
        }
    
        const cursor = this.state.cursor
        const result = this.state.courseSearches
        // arrow up/down button should select next/previous list element
        if (e.keyCode === 38 && cursor > 0) {
          this.setState( prevState => ({
            cursor: prevState.cursor - 1
          }))
        } else if (e.keyCode === 40 && cursor < result.length - 1) {
          //console.log(cursor)
          this.setState( prevState => ({
            cursor: prevState.cursor + 1
          }))
        } // User pressed the enter key
        else if (e.keyCode === 13) {
          e.preventDefault()
          //console.log(this.ref.current.children)
          const suggests = this.ref.current.children;
          const arr = [].slice.call(suggests);
          arr.forEach(function(element) {
            if (element.className === 'suggestions--item active'){
              //console.log("WOOO!!!!!")
              //console.log(element.id)
              submitActive(element.id)
            }
          });
          //console.log("HIT!!!!!!!!!")
        }
    
      }

    handleClose = () => {
        if (!this.state.loading){
            this.setState({
                success: false,
                failure: false,
                alertMessage: ''
            })
        }
        this.props.closeModal()
    }

    selectItem = (title, id) => {
        //console.log(title)
        this.setState({
          input: id,
          showSuggestions: false //THIS IS TENTATIVE, MIGHT BE WORTH REMOVING
        });
      }

    handleClickOff = (e) => {
        if (this.refs.coursesuggestRef.contains(e.target)){
          //console.log(e.target)
          return;
        }
    
        //Close suggestions
        //console.log("HELLO!")
        this.setState({
          showSuggestions: false
        })
      }

    handleClick = (e) => {
        if (this.node.contains(e.target)) {
            //console.log(e.target)
            return;
        }
        // outside click 
        this.handleClose()
    };

    /* Update state as user types in cID*/
    handleCourseIdChange = (e) => {
        this.setState({
          input: e.target.value,
          showSuggestions: true
        }, this.updateProps)
    }

    updateProps = () => {
        if (((this.state.input).toString().length) < 1) {
            this.setState({
                courseSearches: []
            })
            return
        }
        const url = baseurl + 'searchOption/allCourseID/Fall 2019/' + this.state.input
        axios.get(url)
            .then(result => {
            //console.log("YOOO!!!!!")
            //console.log(result['data']['result']);
            this.setState({
                courseSearches: result['data']['result']
            });
        })
    }

    /* Update state as user types in cID*/
    handleURLChange = (e) => {
        this.setState({
            courselinkInput: e.target.value,
        })
    }

    handleSubmit = (e) => {
        e.preventDefault();
        //console.log(this.state);
        //perform axios request here
        this.setState({ loading: true, success: false, failure: false }, () => {
            const url = baseurl + 'course/addData'
            const body = {'course_link': this.state.courselinkInput, 'courseID': this.state.input, 'submit_method' : 'url'};
            axios.post(url, JSON.stringify(body))
              .then(result => {
                //console.log(result);
                this.setState({
                    loading: false,
                    success: true,
                    input: '',
                    courselinkInput: '',
                    alertMessage: ''
                });
            }).catch(error => {
                //console.log(error);
                const err_status = error.response.status
                let alert;
                if (err_status === 404){
                    alert = "You've entered an invalid course"
                } else if (err_status === 401){
                    alert = "The url must be in the JHU domain"
                } else if (err_status === 400){
                    alert = "Please fill out both fields"
                } else{
                    alert = "Sorry, it seems like we were unable to parse your submission, we will be looking into the error in the next few buisness days. Thank you very much for submitting"
                }
                this.setState({
                    loading: false,
                    failure: true,
                    input: '',
                    courselinkInput: '',
                    alertMessage: alert
                });
            });
          });
        //console.log("CLEARED SUBMIT")
        //this.props.addCourseToCal(this.state.id, this.props.currentCalID)
      }

    componentDidMount(){
        document.addEventListener('mousedown', this.handleClick, false);
        document.addEventListener('mousedown', this.handleClickOff, false);
    }

    componentWillUnmount() {
        document.removeEventListener('mousedown', this.handleClick, false);
        document.removeEventListener('mousedown', this.handleClickOff, false);
    }
  
render() {
    const is_alert_success = (!this.state.success) ? "is-display-none" : ''
    const is_alert_failure = (!this.state.failure) ? "is-display-none" : ''

    const showHideClassName = this.props.show ? "modal display-block" : "modal display-none";
    const modalBody = (this.state.loading) ? (<div className="loader"><img  src={loader} alt="Loading..." /></div>) :
        (<div>
            Enter your course number and a link to your class, you will be able to see your data added to your calendar
            and your fellow students will be able to use this data as well. Thank you!
            <br/>
            <br/>
            
            <div className="parse-tool-form">
                <Alert variant='danger' className={is_alert_failure}>
                    {this.state.alertMessage}
                </Alert>
                <Alert variant='success' className={is_alert_success}>
                    Thank you so much for submitting! Your Data has been parsed successfully
                    and your calendar is updating
                </Alert>
                <form ref="coursesuggestRef" style={{width: "100%"}}>
                    <input type="text" value={this.state.input} onChange={this.handleCourseIdChange} onKeyDown={this.handleKeyDown} autoComplete="off" className="margin-bottom-7 width-one-hundred-percent" placeholder="Enter Course ID For Missing data"/>
                    <Suggestions results={this.state.courseSearches} ref={this.ref} select = {this.selectItem} searchOption="ID" show={this.state.showSuggestions} cursor={this.state.cursor} reportModal="yes"/>
                </form>
                <input  type="text"  value={this.state.courselinkInput} onChange={this.handleURLChange} className="width-one-hundred-percent" autoComplete="off" placeholder="Enter course website url"/>
            </div>
            <br/>
            <br/>
        </div>)
    
    const addButton = (this.state.loading) ? (<button type="button" className="btn btn-primary" onClick={this.handleSubmit} disabled>Add</button>
    ) : (<button type="button" className="btn btn-primary" onClick={this.handleSubmit}>Add</button>)
    
    

   return (
    <div id="my-modal" className={showHideClassName}>
    <div  ref={node => this.node = node} className="modal-content">
      <div className="modal-header about-modal-header">
        <span className="center-content"><h2 className="is-size-3">Parse Tool</h2></span>
      </div>
      <div className="modal-body">
        {modalBody}
      </div>
      <div className="modal-footer">
        {addButton}
        <button type="button" className="btn btn-secondary" onClick={this.handleClose}>Close</button>
      </div>
    </div>
  </div>
  );
  }
}

const mapStateToProps = (state) => {
    return{
        show: state.modal.showReportModal,
        currentCalID: state.calendar.currentCalId
    }
}

const mapDispatchToProps = (dispatch) => {
    return{
        closeModal: () => dispatch(closeReportModal()),
        addCourseToCal: (input, id) => dispatch(addCourseToCal(input, id)),
    }
}



export default connect(mapStateToProps, mapDispatchToProps)(ReportModal)