import React from 'react'
import _ from 'lodash'

// for the playstation gamepads, use 1, 0 respectively.
// for the big joystick, use 1, 5.
const AXIS_FB = 1; // which axes control the gamepad
const AXIS_LR = 0;
const AXIS_PIVOT = 5;
const min_speed = 20; //min analog write to the motor drivers
const mmax_speed = 128; //suggested maximum (255 is the physical max)
const lmax_speed = 70; //For the best control
const hmax_speed = 180; // For very fast rover

const joyDead = 0; //Range in wich the joy stick movement is accidental
const joy_max = 100; //Maximum joy stick input
const drive_exp = 1.4; //Relationship between the joystick input and the output (power)

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

  sgn(x) {
    if (x > 0)
      return 1; 
    else if (x < 0)
      return -1; 
    else
      return 0; 
  }

  expdrive(joyVal) {
    let joyMax = joy_max - joyDead; 
    let joySign = this.sgn(joyVal); 
    let joyLive = Math.abs(joyVal) - joyDead

    if (Math.floor(gamepads[driveGamepad].axes[6] == -1)) {
      //Extreme fast mode
      maxSpeed = hmax_speed;
    }
    else if (Math.floor(gamepads[driveGamepad].axes[6] == 1)){
      //Slow mode
      maxSpeed = lmax_speed;
    }
    else{
      //Normal mode
      maxSpeed = mmax_speed;
    }
    //((proportion of the joystick value)^1.4) * range of desired speed + minimum speed
    return (joySign * (min_speed + (maxSpeed-min_speed) * Math.pow(joyLive / joyMax,drive_exp))); 

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

      if(gamepads[driveGamepad].buttons[9].pressed) {
        console.log("ludicrous mode forward")
        fetch(`http://${ServerAddress}:8080/drive/speed/255`, {
          method: 'put'
        })
      }
      
      else if(gamepads[driveGamepad].buttons[8].pressed) {
        console.log("ludicrous mode backward")
        fetch(`http://${ServerAddress}:8080/drive/speed/-255`, {
          method: 'put'
        })
      }

      else if(gamepads[driveGamepad].buttons[0].pressed || (Math.abs(fbSpeed) < 10 && Math.abs(pivotSpeed) < 10 && Math.abs(lrSpeed) < 10)){
        //Stoping mode
        console.log('stopping');
        fetch(`http://${ServerAddress}:8080/drive/stop`, {
          method: 'put'
        })
      }

      
      else if(gamepads[driveGamepad].buttons[1].pressed && Math.abs(pivotSpeed)>10){
        console.log('pivoting 1 ')
        let pSpeed = this.expdrive(pivotSpeed)
        //Pivoting mode
        fetch("http://"+ServerAddress+":8080/drive/pivot/"+ -pSpeed+"/", {
          method: 'put'
        }); 
      }
      
      else {
        console.log('driving mode')
        let lSpeed, rSpeed; 
        //Driving mode
        if(lrSpeed > 10 && fbSpeed > 10){
          //Steering forward/right
          if(fbSpeed >= lrSpeed){
            lSpeed = fbSpeed;
            rSpeed = fbSpeed - lrSpeed;
          }
          //So that the rover doesn't stop at the specified region
          else{
            lSpeed = fbSpeed;
            rSpeed = 0;
          }
          
        }
        else if(lrSpeed > 10 && fbSpeed < 10){
          //Steering backwards right
          if(-fbSpeed >= lrSpeed){
            lSpeed = fbSpeed;
            rSpeed = fbSpeed + lrSpeed;
          }
          else{
            lSpeed = fbSpeed;
            rSpeed = 0;
          }

        }
        else if(lrSpeed < 10 && fbSpeed < 10){
          //Steering backwards left
          if(-fbSpeed >= -lrSpeed){
            lSpeed = fbSpeed - lrSpeed;
            rSpeed = fbSpeed;
            
          }
          else{
            lSpeed = 0;
            rSpeed = fbSpeed;
          }

        }
        else if(lrSpeed < 10 && fbSpeed > 10){
          //Steering forward left
          if(fbSpeed >= -lrSpeed){
            lSpeed = fbSpeed + lrSpeed;
            rSpeed = fbSpeed;
            
          }
          else{
            lSpeed = 0;
            rSpeed = fbSpeed;
          }
        }
        
        lSpeed = Math.floor(this.expdrive(lSpeed))
        rSpeed = Math.floor(this.expdrive(rSpeed))
        
        
        fetch("http://"+ServerAddress+":8080/drive/speed/"+lSpeed+"/" + rSpeed + "/",{
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
