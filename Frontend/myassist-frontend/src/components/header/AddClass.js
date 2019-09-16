import React, { Component } from 'react'
import {connect} from 'react-redux'
import {generateSearchResults, generateSearchResultsProf, generateSearchResultsID} from '../../actions/searchActions'
import {addCourseToCal} from '../../actions/calActions'
import Suggestions from './Suggestions'
import Dropdown from 'react-bootstrap/Dropdown'
import Button from 'react-bootstrap/Button'
import ButtonGroup from 'react-bootstrap/ButtonGroup'
import Alert from 'react-bootstrap/Alert'

class AddClass extends Component {
  state = {
    id: 'null',
    input: '',
    searchOption: 'Title',
    showSuggestions: false,
    cursor: 0
  }
  ref = React.createRef();


  //Deals with downkey nav
  handleKeyDown = (e) => {
    
    const submitActive = (id) => {
      this.setState({
        id: id
      })
    }

    const cursor = this.state.cursor
    const result = this.props.results
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

  changeSearchSetting = (e) => {
    this.setState({
      searchOption: e
    })
  }

  handleChange = (e) => {
    this.setState({
      input: e.target.value,
      showSuggestions: true
    }, this.updateProps)
    
  }

  selectItem = (title, id) => {
    this.setState({
      input: title,
      id: id,
      showSuggestions: false //THIS IS TENTATIVE, MIGHT BE WORTH REMOVING
    });
  }

  updateProps = () => {
    if (this.state.searchOption === "Title"){
      this.props.generateSearchResults(this.state.input)
    } else if (this.state.searchOption === "ID"){
      this.props.generateSearchResultsID(this.state.input)
    } else{
      this.props.generateSearchResultsProf(this.state.input)
    }
    
  }

  handleSubmit = (e) => {
    e.preventDefault();
    //console.log(this.state);
    this.props.addCourseToCal(this.state.id, this.props.currentCalID)
    this.setState({
      id: null,
      input: '',
      showSuggestions: false
    })
  }

  handleClickOff = (e) => {
    if (this.refs.suggestRef.contains(e.target) && e.target.id !== 'dropdown-split-basic'){
      //console.log(e.target)
      return;
    }

    //Close suggestions
    //console.log("HELLO!")
    this.setState({
      showSuggestions: false
    })
  }


  componentDidMount() {
    document.addEventListener('mousedown', this.handleClickOff, false);
  }

  componentWillUnmount() {
    document.removeEventListener('mousedown', this.handleClickOff, false);
  }

  render() {
    //console.log(this.state);
    let placeHolder;
    switch(this.state.searchOption){
      case 'Title':
        placeHolder = "Search by Title"
        break;
      case 'ID':
        placeHolder = "Search by Id"
        break;
      case 'Professor':
        placeHolder = "Search by Professor Name"
        break;
      default:
        break;
    }
    const is_alert = (this.props.alert === '') ? "is-display-none" : 'is-alert'
    return (
        <div>
            <Alert variant='danger' className={is_alert}>
              {this.props.alert}
            </Alert>
            <form ref= "suggestRef" className="add-class--from" onSubmit={this.handleSubmit}>
                <input type="text" autoComplete="off" placeholder={placeHolder} onChange={this.handleChange} onKeyDown={ this.handleKeyDown } value={this.state.input} id="input" className="header-input" />
                <Dropdown as={ButtonGroup} onSelect={this.changeSearchSetting}>
                  <Button variant="outline-success"  className="is-add is-add-button" type="submit">Add</Button>
                  <Dropdown.Toggle split variant="" className="is-add" id="dropdown-split-basic" />
                  <Dropdown.Menu >
                    <Dropdown.Item href="" eventKey='Title'>Course Title</Dropdown.Item>
                    <Dropdown.Item href="" eventKey="ID" >Course Id</Dropdown.Item>
                    <Dropdown.Item href="" eventKey="Professor">Professor Name</Dropdown.Item>
                  </Dropdown.Menu>
                  </Dropdown>
                <Suggestions results={this.props.results} ref={this.ref} select = {this.selectItem} searchOption={this.state.searchOption} show={this.state.showSuggestions} cursor={this.state.cursor} reportModal="no"/>
            </form>
        </div>
    )
  }
}


const mapStateToProps = (state) => {
    return{
      results: state.search.searches,
      currentCalID: state.calendar.currentCalId,
      alert: state.calendar.alert
    }
  }

const mapDispatchToProps = (dispatch) => {
  return {
    generateSearchResults: (input) => dispatch(generateSearchResults(input)),
    addCourseToCal: (input, id) => dispatch(addCourseToCal(input, id)),
    generateSearchResultsID: (input) => dispatch(generateSearchResultsID(input)),
    generateSearchResultsProf: (input) => dispatch(generateSearchResultsProf(input)),
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(AddClass)
