import authReducer from './authReducer'
import calReducer from './calReducer'
import modalReducer from './modalReducer'
import searchReducer from './searchReducer'
import displayReducer from './displayReducer'
import { combineReducers } from 'redux'

const rootReducer = combineReducers({
  auth: authReducer,
  calendar: calReducer,
  modal: modalReducer,
  search: searchReducer,
  display: displayReducer
});

export default rootReducer