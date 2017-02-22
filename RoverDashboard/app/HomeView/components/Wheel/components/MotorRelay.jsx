import React from 'react'

class MotorRelay extends React.Component {

  constructor(props) {
    super(props)
    this.state = {
      index: this.props.index,
      status: this.props.status
    }
    this.updateServer = this.updateServer.bind(this)
  }

  componentWillReceiveProps(newProps) {
		this.setState({
			status: this.props.status
		})
	}

  updateServer() {

    fetch("http://"+ServerAddress+":8080/aux/relay/"+this.props.index+"/"+!this.props.status, {
      method: 'put'
    }).then((response) => {
      if(response.ok){
        console.log("Status for Motor " + this.props.index + " was updated")
      }
      else {
        console.log("Status for Motor " + this.props.index + " could not update")
      }
    }).catch((error) => {
        console.log("Cannot Reach Server")
    })
  }

  render() {
    return(
      <div>
        {!this.state.status && <button className="btn btn-danger" onClick={this.updateServer}>Motor: Off</button>}
        {this.state.status && <button className="btn btn-success" onClick={this.updateServer}>Motor: On</button>}
      </div>

    )
  }
}

export default MotorRelay
