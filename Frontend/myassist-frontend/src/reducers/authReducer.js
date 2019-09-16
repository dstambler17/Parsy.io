const initState = {
    authError: null,
    user: null,
    isSignedIn: false,
    profilePic: null,
    signedincalID: null,
    id_token: null
}

const authReducer = (state = initState, action) => {
    switch(action.type){
        case 'LOGIN_ERROR':
          //console.log('login error');
          return {
            ...state,
            authError: 'Login failed'
          }
    
        case 'LOGIN_SUCCESS':
          //console.log('login success');
          return {
            ...state,
            authError: null,
            user: action.user,
            isSignedIn: true,
            signedincalID: action.calid,
            profilePic: action.userPic,
            id_token: action.id_token
          }
    
        case 'LOGOUT_SUCCESS':
          //console.log('logout success');
          return {
            ...state,
            user: null,
            isSignedIn: false,
            profilePic: null,
            signedincalID: null,
            id_token: null
          };
    
        case 'SIGNUP_SUCCESS':
          //console.log('signup success')
          return {
            ...state,
            authError: null
          }
    
        case 'SIGNUP_ERROR':
          //console.log('signup error')
          return {
            ...state,
            authError: action.err.message
          }
        
        case 'NULL_SIGNED_CAL':
          return{
            ...state,
            signedincalID: null
          }
    
        default:
          return state
      }
}

export default authReducer