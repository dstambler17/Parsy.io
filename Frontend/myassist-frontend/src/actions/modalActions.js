export const showAboutModal = () => {
    return{
        type: "SHOW_ABOUT_MODAL"
    }
}

export const closeAboutModal = () => {
    return{
        type: "CLOSE_ABOUT_MODAL"
    }
}

export const showHowToModal = () => {
    return{
        type: "SHOW_HOW_TO_USE_MODAL"
    }
}

export const closeHowToModal = () => {
    return{
        type: "CLOSE_HOW_TO_USE_MODAL"
    }
}

export const showLogInSignUpModal = () => {
    return{
        type: "SHOW_LOGIN_SIGNUP_MODAL"
    }
}

export const closeLogInSignUpModal = () => {
    return{
        type: "CLOSE_LOGIN_SIGNUP_MODAL"
    }
}

export const showReportModal = () => {
    return{
        type: "SHOW_REPORT_MODAL"
    }
}

export const closeReportModal = () => {
    return{
        type: "CLOSE_REPORT_MODAL"
    }
}

export const showSaveModal = () => {
    return{
        type: "SHOW_SAVE_MODAL"
    }
}

export const closeSaveModal = () => {
    return{
        type: "CLOSE_SAVE_MODAL"
    }
}


export const showTimeSlotModal = (title, start, end) => {
    return{
        type: "SHOW_TIMESLOT_MODAL",
        title: title,
        start: start,
        end: end
    }
}

export const closeTimeSlotModal = () => {
    return{
        type: "CLOSE_TIMESLOT_MODAL"
    }
}