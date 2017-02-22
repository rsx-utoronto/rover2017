import React from 'react';
import io from 'socket.io-client'

class KeepAlive extends React.Component {

  constructor(props) {
    super(props)
    this.state = {
      socket: null,
      connection: 'Not Connected'
    }
    this.onConnect = this.estalishKeepAlive.bind(this)
    this.toDisconnect = this.disableKeepAlive.bind(this)
  }

  estalishKeepAlive() {
    console.log("Establishing Keep Alive")
    this.setState({
      socket: io.connect("localhost:8080"),
      connection: 'Connected'
    })

  }

  disableKeepAlive() {
    console.log("Disabling Keep Alive")
    this.setState({
      socket: null,
      connection: 'Not Connected'
    })

  }

  render() {
    if(this.state.connection == 'Not Connected'){
      return(
        <button onClick={this.onConnect}>
          Connect
        </button>
      )
    }
    else {
      return(
        <button onClick={this.toDisconnect}>
          Disconnect
        </button>
      )
    }

  }


}

export default KeepAlive
