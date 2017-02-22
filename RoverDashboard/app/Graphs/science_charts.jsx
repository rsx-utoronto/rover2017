import React from 'react'
import RTChart from 'react-rt-chart'

export default class ScienceCharts extends React.Component {

  constructor(props) {
      super(props)
  }

  componentDidMount() {
    this.interval = setInterval(() => this.forceUpdate(), 1000)
  }

  componentWillUnmount() {
    clearInterval(this.interval)
  }

  render() {
      var data = {
        date: new Date(),
        Humidity: Math.random(),
        Temperature: Math.random(),
        Other: Math.random()
      }

      return(
        <div>
          <RTChart fields={['Humidity', 'Temperature', 'Other']} data={data} maxValues={20}/>
          <RTChart fields={['Temperature']} data={data} maxValues={20}/>
        </div>
      )
  }

}
