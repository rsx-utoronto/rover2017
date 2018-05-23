import React from 'react'
import _ from 'lodash'

// AXIS ASSIGNMENTS
// for the big joystick, use 1, 5.
const AXIS_FB = 1; // which axes control the rover's forward/ backward motion
const AXIS_LR = 0; // which axis controls the rover's left/ right motion
const AXIS_PIVOT = 5; // which axis controls the rover's pivot. by default, this is disabled.
const AXIS_SPEED = 6; // which axis controls the rover's speed

// BUTTON ASSIGNMENTS
const STOP_BTN                = 0;
const ENABLE_PIVOT_BUTTON     = 1;
const LUDICROUS_BACKWARD_BTN  = 8;
const LUDICROUS_FORWARD_BTN   = 9;

// DRIVE PARAMETERS READ FROM CONFIG
// These are the default values, do not change them in your code.
var minSensitivity = 70; // maximum speed when sensitivity is minimized.
var maxSensitivity = 180; // ^ sensitivity is maximized

// MISCELLANEOUS DRIVE PARAMETERS
const JOYSTICK_DEADZONE = 0.15;
const DRIVE_EXP = 1.4; // the power of the output will be joystickValue ** 1.4

let state; // save state on dismount
let interval; // handles drive

export default class Setup extends React.Component {
  constructor(props) {
    super(props)
    console.log(props);
    console.log(props.minSensitivity);

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

    // fetch('localhost:8080/config.json')
    // .then(config => config.json())
    // .then(config => {
    //   if (config.minSensitivity !== undefined)
    //     minSensitivity = config.minSensitivity;
    //   if (config.maxSensitivity !== undefined)
    //     maxSensitivity = config.maxSensitivity;
    // })
    // .catch(console.warn);
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

    let gp = this.state.joystickPositions[index];
    if (gp.axes.length < 4) {
      return <div>Invalid joystick</div>
    }
    else {
      return <div>
        forward: {gp.axes[AXIS_FB].toFixed(4)} <br/>
        pivot: {gp.axes[AXIS_PIVOT].toFixed(4)}
      </div>
    }
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

  /**
    Takes joyVal, a raw value from the joystick and converts it to a the speed for the rover.

    joyVal should be a value from -1 to 1.
    speedControl should be a value from -1 to 1, representing how sensitive the joystick is ranging from minSensitivity to maxSensitivity

    The output is in the range -255 to 255.
  */
  expdrive(joyVal, speedControl) {
    if(joyVal == 0) {
      return 0;
    }

    // set the maximum speed as controlled by the SPEED_AXIS
    let joyMax = (speedControl + 1) / 2 * (maxSensitivity - minSensitivity) + minSensitivity;

    // ((proportion of the joystick value)^1.4) * range of desired speed + minimum speed
    if(_.isNaN(this.sgn(joyVal) * joyMax * Math.pow(Math.abs(joyVal), 1.4))){
      console.log(joyVal)
    }
    return this.sgn(joyVal) * joyMax * Math.pow(Math.abs(joyVal), 1.4);
  }

  updateDriveGamepadPoller() {
    clearInterval(interval);
    interval = setInterval(() => {
      let driveGamepadId = this.state.joystickMapping.indexOf('drive');

      if (driveGamepadId === -1)  // nothing listening to drive
        return

      let gamepads = navigator.getGamepads()
      let driveGamepad = gamepads[driveGamepadId];
      if (!driveGamepad) {
        console.error(`No game pad connected to port ${driveGamepadId}`)
        return
      }

      let fbSpeed = driveGamepad.axes[AXIS_FB] * -1;
      let lrSpeed = driveGamepad.axes[AXIS_LR];
      let pivotSpeed = driveGamepad.axes[AXIS_PIVOT] * -1;
      let speedControl = driveGamepad.axes[AXIS_SPEED] * -1;

      if(driveGamepad.buttons[STOP_BTN].pressed) {
        fetch(`http://${ServerAddress}/drive/stop`, {
          method: 'put'
        });
      }

      // Ludicrous forward: full speed
      else if(driveGamepad.buttons[LUDICROUS_FORWARD_BTN].pressed) {
        console.log("ludicrous mode forward");
        fetch(`http://${ServerAddress}/drive/speed/255`, {
          method: 'put'
        });
      }

      // Ludicrous backward: full speed
      else if(driveGamepad.buttons[LUDICROUS_BACKWARD_BTN].pressed) {
        console.log("ludicrous mode backward");
        fetch(`http://${ServerAddress}/drive/speed/-255`, {
          method: 'put'
        });
      }

      // Pivot
      else if(driveGamepad.buttons[ENABLE_PIVOT_BUTTON].pressed && Math.abs(pivotSpeed) > JOYSTICK_DEADZONE){
        let pSpeed = this.expdrive(pivotSpeed, speedControl);
        fetch(`http://${ServerAddress}/drive/pivot/${pSpeed}`, {
          method: 'put'
        });
      }

      // Drive normally
      //    FRONT
      //  \   1   /
      //    \   /
      //  4   X   3
      //    /   \
      //  /   2   \
      //
      // When the joystick is in regions 1 or 2, one wheel turns faster than the other
      // When the joystick is in regions 3 and 4, only one wheel turns.
      else if (Math.abs(lrSpeed) > JOYSTICK_DEADZONE || Math.abs(fbSpeed) > JOYSTICK_DEADZONE) {
        let lSpeed, rSpeed;
        if (lrSpeed > 0) {
          lSpeed = fbSpeed;
          if (Math.abs(fbSpeed) >= Math.abs(lrSpeed)) {
            rSpeed = Math.abs(fbSpeed) - lrSpeed;
          }
          else {
            rSpeed = 0;
          }
        }
        else {
          rSpeed = fbSpeed;
          if (Math.abs(fbSpeed) >= Math.abs(lrSpeed)) {
            lSpeed = -Math.abs(fbSpeed) - lrSpeed;
          }
          else {
            lSpeed = 0;
          }
        }
        lSpeed = Math.floor(this.expdrive(lSpeed, speedControl));
        rSpeed = Math.floor(this.expdrive(rSpeed, speedControl));
        fetch(`http://${ServerAddress}/drive/speed/${lSpeed}/${rSpeed}`, {
          method: 'put'
        });
      }

      else {
        // Stop
        fetch(`http://${ServerAddress}/drive/stop`, {
          method: 'put'
        });
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
            fetch(`http://${ServerAddress}/${systemName}/tcp"`)
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
