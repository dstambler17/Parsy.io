const initState = {
    mobileBottomDisplay: false,
    threeDayWeek: false
}

const displayReducer = (state = initState, action) => {
    switch(action.type){
        case 'SHOW_BOTTOM_TAB':
            return {
                ...state,
                mobileBottomDisplay : true
            }
        case 'HIDE_BOTTOM_TAB':
            return {
                ...state,
                mobileBottomDisplay : false
            }
        case 'SET_THREE_DAY_WEEK':
            return {
                ...state,
                threeDayWeek: true
            }
        case 'SET_SEVEN_DAY_WEEK':
            return {
                ...state,
                threeDayWeek: false
            }
        default:
            return state
    }
}

export default displayReducer