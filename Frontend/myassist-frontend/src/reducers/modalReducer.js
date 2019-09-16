const initState = {
    showAboutModal: false,
    showHowToModal: false,
    showLoginSignUpModal: false,
    showReportModal: false,
    showSaveCalModal: false,
    showSettingsModal: false,
    showtimeSlotModal: false,
    timeSlotModalTitle: null,
    timeSlotstartTime: null,
    timeSlotendTime: null

}

const modalReducer = (state = initState, action) => {
    switch(action.type){
        case 'SHOW_ABOUT_MODAL':
            return {
                ...state,
                showAboutModal: true,
            }
        case 'CLOSE_ABOUT_MODAL':
            return {
                ...state,
                showAboutModal: false,
            }
        case 'SHOW_HOW_TO_USE_MODAL':
            return {
                ...state,
                showHowToModal: true,
            }
        case 'CLOSE_HOW_TO_USE_MODAL':
            return {
                ...state,
                showHowToModal: false,
            }
        case 'SHOW_LOGIN_SIGNUP_MODAL':
            return {
                ...state,
                showLoginSignUpModal: true,
            }
        case 'CLOSE_LOGIN_SIGNUP_MODAL':
            return {
                ...state,
                showLoginSignUpModal: false,
            }
        case 'SHOW_REPORT_MODAL':
            return {
                ...state,
                showReportModal: true,
            }
        case 'CLOSE_REPORT_MODAL':
            return {
                ...state,
                showReportModal: false,
            }
        case 'SHOW_SAVE_MODAL':
            return {
                ...state,
                showSaveCalModal: true,
            }
        case 'CLOSE_SAVE_MODAL':
            return {
                ...state,
                showSaveCalModal: false,
            }
        case 'SHOW_TIMESLOT_MODAL':
            return {
                ...state,
                showtimeSlotModal: true,
                timeSlotModalTitle: action.title,
                timeSlotstartTime: action.start,
                timeSlotendTime: action.end
            }
        case 'CLOSE_TIMESLOT_MODAL':
            return {
                ...state,
                showtimeSlotModal: false,
                timeSlotModalTitle: null,
                timeSlotstartTime: null,
                timeSlotendTime: null
            }
        default:
            return state
    }
}

export default modalReducer