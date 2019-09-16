import React from 'react'

const Suggestions = React.forwardRef((props, ref) => {

  const handleClick = (e) => {
    //console.log(e.target.id)
    let id = e.target.id
    const title = props.results.filter(res => {
      return res.id === id
    });
    //console.log("WOOP")
    //console.log(title[0].Name)
    props.select(title[0].Name, id)
  }

  const type = (props.searchOption === "Professor") ? "Instructor" : "Name"
  const options = (props.results.length > 0) ? (props.results.map((r, i) => (
    <div key={r.id} id={r.id}  onClick={handleClick} className={props.cursor === i ? 'suggestions--item active' : "suggestions--item"}>
      {r[type]} -- {r.id}
    </div>
  ))) : null

  const reportPosition = (props.reportModal === "yes") ? "suggestions--list suggestions-list-report" : "suggestions--list"
  const optionsClass = (options !== null && props.show) ? reportPosition : reportPosition +  " is-display-none"
  return (<div ref={ref} className={optionsClass}>{options}</div>)
})

export default Suggestions
