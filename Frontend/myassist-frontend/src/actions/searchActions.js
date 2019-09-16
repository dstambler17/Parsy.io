import {baseurl} from '../constants.js'

export const generateSearchResults = (input) => {
    if ((input.toString().length) < 1) {
        return (dispatch) => {dispatch({type: 'GET_LIST_ERROR'})}
    }
    return (dispatch) => {
        let url = baseurl + 'searchOption/className/Fall 2019/'+ input
        return fetch(url)
        .then(res => res.json()).then((resp) => {
            dispatch({ type: 'GET_LIST_SUCCESS', list: resp });
          })
    }
};

export const generateSearchResultsID = (input) => {
    if ((input.toString().length) < 1) {
        return (dispatch) => {dispatch({type: 'GET_LIST_ERROR'})}
    }
    return (dispatch) => {
        let url = baseurl + 'searchOption/courseID/Fall 2019/'+ input
        return fetch(url)
        .then(res => res.json()).then((resp) => {
            dispatch({ type: 'GET_LIST_SUCCESS', list: resp });
          })
    }
};

export const generateSearchResultsProf = (input) => {
    if ((input.toString().length) < 1) {
        return (dispatch) => {dispatch({type: 'GET_LIST_ERROR'})}
    }
    return (dispatch) => {
        let url = baseurl + 'searchOption/instName/Fall 2019/'+ input
        return fetch(url)
        .then(res => res.json()).then((resp) => {
            dispatch({ type: 'GET_LIST_SUCCESS', list: resp });
          })
    }
};