import React from 'react';
import TimeGrid from 'react-big-calendar/lib/TimeGrid';

class ThreeDayWeek extends React.Component {
    render() {
      let { date } = this.props
      let range = ThreeDayWeek.range(date)
  
      return <TimeGrid {...this.props} range={range} eventOffset={15} />
    }
  }
  

  export default ThreeDayWeek