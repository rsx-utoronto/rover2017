import React from 'react'
import RTChart from 'react-rt-chart'

export default class ScienceCharts extends React.Component {

  constructor(props) {
      super(props)
  }

  componentDidMount() {
    this.interval = setInterval(() => this.forceUpdate(), 1500)
  }

  componentWillUnmount() {
    clearInterval(this.interval)
  }

  render() {
    var data = {
      date: new Date(),
      Humidity: 0,
      Temperature: 0,
      Gas: 0
    }

    fetch("http://"+ServerAddress+"/science").then((response) => {
      if (response.ok) {
        response.json().then((jsonRes) => {
          data.Humidity = jsonRes.humidity
          data.Temperature = jsonRes.outer_temp
          data.Gas = jsonRes.gas
        })
      } else {
        console.log("Network Response Not OK (/science)")
      }
    }).catch((error) => {
      console.log("Cannot Reach Science Endpoint '/science'")
    })

    var RandData = {
      date: new Date(),
      Humidity: Math.random(),
      Temperature: Math.random(),
      Gas: Math.random()
    }

    return(
      <div>
        <RTChart fields={['Humidity', 'Temperature', 'Gas']} data={data} maxValues={20}/>
        <RTChart fields={['Humidity', 'Temperature', 'Gas']} data={RandData} maxValues={20}/>
      </div>
    )
  }

}
