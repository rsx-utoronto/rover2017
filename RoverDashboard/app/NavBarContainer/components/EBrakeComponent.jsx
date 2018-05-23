import React from 'react'
import {Button} from 'react-bootstrap'

export default class EBrakeComponent extends React.Component {

  constructor(props) {
    super(props)
    this.state ={
      enable: false
    }
    this.toggleEBrake = this.toggleEBrake.bind(this)
  }

  componentDidMount() {
    this.interval = setInterval(() => this.updateData(), 1000)
  }

  componentWillUnmount() {
    clearInterval(this.interval)
  }

  updateData() {
    fetch("http://"+ServerAddress+"/drive/ebrake").then((response) => {
      if(response.ok){
        response.json().then((myJSON) => {
          this.setState({
            enable: myJSON.ebrake
          })
        })
      } else {
        console.log("Network response not ok")
      }
    }).catch((error) => {
      console.log("[Error]: EBrakeComponent unable to get ebrake status")
    })
  }

  toggleEBrake() {
    fetch("http://"+ServerAddress+"/drive/ebrake",{
      method: 'put'
    })
  }

  render() {
    if (this.state.enable) {
      return(
        <div>
          <Button bsStyle="danger" onClick={this.toggleEBrake}>E-Brake: Engaged</Button>
        </div>
      )
    } else {
      return(
        <div>
          <Button bsStyle="danger" onClick={this.toggleEBrake}>E-Brake: Disengaged</Button>
        </div>
      )
    }
  }
}
