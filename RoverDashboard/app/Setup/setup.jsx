import React from 'react'
import _ from 'lodash'

// for the playstation gamepads, use 1, 0 respectively.
// for the big joystick, use 1, 5.
const AXIS_FB = 1; // which axes control the gamepad
const AXIS_LR = 5;
const AXIS_PIVOT = 0;

let state; // save state on dismount
let interval; // handles drive

export default class Setup extends React.Component {
  constructor(props) {
    super(props)

    this.state = state ? state : {
      joystickMapping: _.map(navigator.getGamepads(), () => 'n/a'), // {joystick: system} mapping.
      joystickPositions: navigator.getGamepads(),
      interval: undefined
    };

    this.joystickSystems = ['drive', 'arm'];

    this.componentDidMount = this.componentDidMount.bind(this);
    this.gamepadRow = this.gamepadRow.bind(this);
    this.bindGamepad = this.bindGamepad.bind(this);
    this.updateDriveGamepadPoller = this.updateDriveGamepadPoller.bind(this);
    this.summarizeGamepad = this.summarizeGamepad.bind(this);
    this.updateJoystickPosition = this.updateJoystickPosition.bind(this);
  }

  componentDidMount() {
    // update the ui element to see joystick positions
    this.interval = setInterval(() => this.updateJoystickPosition(), 100);
  }

  componentWillUnmount() {
    state = this.state;
    clearInterval(this.interval);
	}

  updateJoystickPosition() {
    this.setState({joystickPositions: navigator.getGamepads()});
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
      forward: {gp.axes[AXIS_FB].toFixed(4)} <br/>
      pivot: {gp.axes[AXIS_PIVOT].toFixed(4)}
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
            <button className='btn btn-sm' data-toggle='dropdown'>
              {this.state.joystickMapping[index]}
              <span className='caret'> </span>
            </button>
            <ul className='dropdown-menu'>
              {this.joystickSystems.map((sys) => (
                <li key={sys} onClick={() => this.bindGamepad(index, sys)}> <a> {sys} </a> </li>
              ))}
            </ul>
          </div>
        </td>
      </tr>
    )
  }

  updateDriveGamepadPoller() {
    clearInterval(interval);
    interval = setInterval(() => {
      let driveGamepad = this.state.joystickMapping.indexOf('drive');
      if (driveGamepad === -1)  // nothing listening to drive
        return
      let gamepads = navigator.getGamepads()
      if (!gamepads[driveGamepad]) {
        console.error(`No game pad connected to port ${driveGamepad}`)
        return
      }

      let fbSpeed = Math.floor(gamepads[driveGamepad].axes[AXIS_FB] * -100)
      let lrSpeed = Math.floor(gamepads[driveGamepad].axes[AXIS_LR] * 100)
      let pivotSpeed = Math.floor(gamepads[driveGamepad].axes[AXIS_PIVOT] * 100)

      if(gamepads[driveGamepad].buttons[8].pressed) {
        console.log("ludicrous mode")
        fetch(`http://${ServerAddress}:8080/drive/speed/255`, {
          method: 'put'
        })
      }
      
      else if(gamepads[driveGamepad].buttons[1].pressed || (Math.abs(fbSpeed) < 10 && Math.abs(pivotSpeed) < 10 && Math.abs(lrSpeed) < 10)){
        //Stoping mode
        fetch(`http://${ServerAddress}:8080/drive/stop`, {
          method: 'put'
        })
      }

      
      else if(gamepads[driveGamepad].buttons[0].pressed){
        //Pivoting mode
        fetch("http://"+ServerAddress+":8080/drive/pivot/"+pivotSpeed+"/", {
          method: 'put'
        })
      }
      

      else {
        //Driving mode
        if(lrSpeed > 10 && fbSpeed > 10){
          //Steering forward/right
          if(fbSpeed >= lrSpeed){
            let lSpeed = fbSpeed;
            let rSpeed = fbSpeed - lrSpeed;
            fetch("http://"+ServerAddress+":8080/drive/speed/"+lSpeed+"/" + rSpeed + "/",{
            method: 'put'
            })
          }
          else{
            let lSpeed = lrSpeed;
            let rSpeed = -100 + fbSpeed;
            fetch("http://"+ServerAddress+":8080/drive/speed/"+lSpeed+"/" + rSpeed + "/",{
            method: 'put'
            })
          }
        }
        else if(lrSpeed > 10 && fbSpeed < 10){
          //Steering backwards right
          if(-fbSpeed >= lrSpeed){
            let lSpeed = fbSpeed;
            let rSpeed = fbSpeed + lrSpeed;
            fetch("http://"+ServerAddress+":8080/drive/speed/"+lSpeed+"/" + rSpeed + "/",{
            method: 'put'
            })
          }
          else{
            let lSpeed = -lrSpeed;
            let rSpeed = -100 - fbSpeed;
            fetch("http://"+ServerAddress+":8080/drive/speed/"+lSpeed+"/" + rSpeed + "/",{
            method: 'put'
            })
          }
        }
        else if(lrSpeed < 10 && fbSpeed < 10){
          //Steering backwards left
          if(-fbSpeed >= -lrSpeed){
            let lSpeed = fbSpeed - lrSpeed;
            let rSpeed = fbSpeed;
            fetch("http://"+ServerAddress+":8080/drive/speed/"+lSpeed+"/" + rSpeed + "/",{
            method: 'put'
            })
          }
          else{
            let lSpeed = 100 + fbSpeed;
            let rSpeed = lrSpeed;
            fetch("http://"+ServerAddress+":8080/drive/speed/"+lSpeed+"/" + rSpeed + "/",{
            method: 'put'
            })
          }
          
        }
        else if(lrSpeed < 10 && fbSpeed > 10){
          //Steering forward left
          if(fbSpeed >= -lrSpeed){
            let lSpeed = fbSpeed + lrSpeed;
            let rSpeed = fbSpeed;
            fetch("http://"+ServerAddress+":8080/drive/speed/"+lSpeed+"/" + rSpeed + "/",{
            method: 'put'
            })
          }
          else{
            let lSpeed = -100 + fbSpeed;
            let rSpeed = -lrSpeed;
            fetch("http://"+ServerAddress+":8080/drive/speed/"+lSpeed+"/" + rSpeed + "/",{
            method: 'put'
            })
          }
        }
        
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
            fetch("http://"+ServerAddress+":8080/"+systemName+"/tcp")
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
