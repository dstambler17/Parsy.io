import React from 'react';
import { BrowserRouter, Switch, Route } from 'react-router-dom'
import MainBody from './components/calendar/MainBody'
import SuggestedUploads from './components/uploads/SuggestedUploads'
import { withCookies } from 'react-cookie';

function App(props) {
  return (
    <BrowserRouter>
      <div className="App">
        <Switch>
          <Route exact path = '/' render={() => (<MainBody cookies={props.cookies}/>)}/>
          <Route path ='/uploadForm' component = {SuggestedUploads}/>
        </Switch>
      </div>
    </BrowserRouter>
  );
}

export default withCookies(App);
