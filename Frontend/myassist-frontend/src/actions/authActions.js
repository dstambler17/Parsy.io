import {baseurl} from '../constants.js'

export const logIn = (creds, calid) => (dispatch) =>{
    const info = {"calid": calid, "creds" : creds}
    //console.log(creds)
    //console.log(calid)

    fetch(baseurl + 'user/GSignIn', {
        method: 'POST',
        body: JSON.stringify(info),
        headers: {
            'Content-Type': 'application/json'
        },
      }).then(res => res.json()).then(response => {
          //console.log(response['id_token'])
        return dispatch({
            type: "LOGIN_SUCCESS",
            user: response['id_token']['name'],
            userPic: response['id_token']['picture'],
            calid: response['calId'],
            id_token: response['id_token']
        })
    }).catch(error => console.error('Error', error))

}


export const logInReload = (name, pic, userid, id_token, calID) => (dispatch) =>{
    const info = {"calid": calID, "userid" : userid}
    ////console.log(info)
    ////console.log(calid)

    fetch(baseurl + 'user/GSignInPageReload', {
        method: 'POST',
        body: JSON.stringify(info),
        headers: {
            'Authorization': id_token,
            'Content-Type': 'application/json'
        },
      }).then(res => res.json()).then(response => {
        return dispatch({
            type: "LOGIN_SUCCESS",
            user: name,
            userPic: pic,
            calid: response['calId'],
            id_token: id_token
        })
    }).catch(error => console.error('Error', error))

}



export const logOut = () => {
    return {
        type: "LOGOUT_SUCCESS"
    }
}

export const nullSignedInCal = () => {
    return {
        type: "NULL_SIGNED_CAL"
    }
}