import React from 'react'
import _ from 'lodash'

export default class Setup extends React.Component {
  constructor(props) {
    super(props)

    var joystickMapping = _.map(navigator.getGamepads(), () => 'n/a') // {joystick: system} mapping.

    this.state = {
      joystickMapping: joystickMapping,
      joystickPositions: navigator.getGamepads()
    }

    this.joystickSystems = ['drive', 'arm']

    this.gamepadRow = this.gamepadRow.bind(this)
    this.bindGamepad = this.bindGamepad.bind(this)
    this.updateDriveGamepadPoller = this.updateDriveGamepadPoller.bind(this)
    this.summarizeGamepad = this.summarizeGamepad.bind(this)
    this.updateJoystickPosition = this.updateJoystickPosition.bind(this)

  }

  componentDidMount() {
    // update the ui element to see joystick positions
    this.interval = setInterval(() => this.updateJoystickPosition(), 100)
  }

  componentWillUnmount() {
		clearInterval(this.interval)
	}

  updateJoystickPosition() {
    this.setState({joystickPositions: navigator.getGamepads()})
  }

  bindGamepad(index, system) {
    // binds gamepad[index] to system. also ensures that only one
    // system is connected at once
    let newMapping = this.state.joystickMapping.map((js, i) =>
      js == system ? 'n/a' : js
    )
    newMapping[index] = system
    this.setState({joystickMapping: newMapping}, () => {
      this.updateDriveGamepadPoller()
    })
  }

  summarizeGamepad(index) {
    if(!this.state.joystickPositions || !this.state.joystickPositions[index])
      return <div></div>

    let gp = this.state.joystickPositions[index]
    return <div>
      forward: {gp.axes[1]} <br/>
      pivot: {gp.axes[5]}
    </div>
  }

  gamepadRow(gamepad, index) {
    return (
      <tr key={gamepad ? gamepad.id : index}>
        <td className='joystick-label'> Joystick {index} </td>
        <td className='joystick-axes'>
          {this.summarizeGamepad(index)}
        </td>
        <td>
          <div className='dropdown'>
            <button data-toggle='dropdown'>
              {this.state.joystickMapping[index]}
              <span className='caret'> </span>
            </button>
            <ul className='dropdown-menu'>
              {this.joystickSystems.map((sys) => (
                <li key={sys} onClick={() => this.bindGamepad(index, sys)}> {sys} </li>
              ))}
            </ul>
          </div>
        </td>
      </tr>
    )
  }

  updateDriveGamepadPoller() {
    let driveGamepad = this.state.joystickMapping.indexOf('drive')
    if (driveGamepad === -1)  // nothing listening to drive
      return
    let gamepads = navigator.getGamepads()
    if (!gamepads[driveGamepad]) {
      console.error(`No game pad connected to port ${driveGamepad}`)
      return
    }

    clearInterval(this.interval)
    this.interval = setInterval(() => {
      let fbSpeed = Math.floor(gamepads[driveGamepad].axes[1] * -255)
      let pivotSpeed = Math.floor(gamepads[driveGamepad].axes[5] * -255)

      if(Math.abs(fbSpeed) > Math.abs(pivotSpeed)) {
        fetch("http://"+ServerAddress+":8080/drive/speed/"+fbSpeed+"/",{
          method: 'put'
        })
      }
      else {
        fetch("http://"+ServerAddress+":8080/drive/pivot/"+pivotSpeed+"/", {
          method: 'put'
        })
      }
    }, 50)
  }

  createConnectRow(systemName) {
    return (
      <tr key={systemName}>
        <td className='tcp-connect-title'> {_.capitalize(systemName)} Arduino </td>
        <td className='tcp-connect-btn'>
          <button className='btn btn-sm btn-primary'
          onClick={() => {
            fetch("http://"+ServerAddress+":8080/${systemName}/tcp")
          }}
          > Connect! </button>
        </td>
      </tr>
    )
  }

  render() {
    return (
      <div className='setup-page'>
        <div className='container tcp-connect'>
          <table className='table-bordered'>
            <thead>
              <tr>
                <th> Subsystem </th>
                <th> Server-Arduino </th>
              </tr>
            </thead>
            <tbody>
              {['drive', 'arm', 'sensor', 'aux'].map(this.createConnectRow)}
            </tbody>
          </table>
        </div>

        <div className='container joystick-config'>
          <table className='table-bordered'>
            <thead>
              <tr>
                <th> </th>
                <th> Readings </th>
                <th> Controlling </th>
              </tr>
            </thead>
            <tbody>
              {_.map(navigator.getGamepads()).map(this.gamepadRow)}
            </tbody>
          </table>
        </div>
      <br/>
      </div>
    )
  }
}
