const initState = {
    searches: []
}

const searchReducer = (state = initState, action) => {
    switch(action.type){
        case 'GET_LIST_SUCCESS':
            //console.log(action.list.result)
            return {searches : action.list.result}
        case 'GET_LIST_ERROR':
            return {searches : []}
        default:
            return state
    }
}

export default searchReducer