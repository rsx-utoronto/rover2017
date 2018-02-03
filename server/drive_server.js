var express = require('express');
var _ = require('lodash');
var net = require('net');
var SerialPort = require('serialport');

var client = undefined; // arduino tcp client
var port = undefined;

function init(model, config) {
    model.drive = {
        speed: [
            0, 0
        ], // -255 to 255
        pivot: 0,
        drive_mode: true, // drive mode vs pivot mode
        ebrake: false,
        connected: false
    }

    var router = express.Router();

    // gets rover speed and turning parameters
    router.get('/', (req, res) => {
        res.json(model.drive);
    })

    // sets rover forward speed.
    router.put('/speed/:speed', (req, res) => {

        if(!model.drive.ebrake) {
          model.drive.speed[0] = model.drive.speed[1] = parseInt(req.params.speed);
          model.drive.drive_mode = true;
          res.json(model.drive);
          
          if(model.verbose) { 
            console.log("Sending speed ", req.params.speed); 
          }
        } else {
          res.status(500).send("EBrake Enabled")
        }

    });

    // sets rover speed on both wheels.
    router.put('/speed/:speed0/:speed1', (req, res) => {
        if(!model.drive.ebrake) {
          model.drive.speed[0] = parseInt(req.params.speed0);
          model.drive.speed[1] = parseInt(req.params.speed1);
          model.drive.drive_mode = true;
          res.json(model.drive);
        } else {
          res.status(500).send("EBrake Enabled")
        }

    });

    // sets the pivot speed of the rover. pivoting requires us to turn off
    // the middle wheels or the rocker bogie dies.
    router.put('/pivot/:turn_speed', (req, res) => {
      if(!model.drive.ebrake) {
        model.drive.pivot = parseInt(req.params.turn_speed);
        model.drive.drive_mode = false;
        res.json(model.drive);
      } else {
        res.status(500).send("EBrake Enabled")
      }

    });

    router.put('/stop', (req, res) => {
        model.drive.speed[0] = model.drive.speed[1] = 0;
        model.drive.pivot = 0;
        res.json(model.drive);
    });

    router.get('/ebrake', (req, res) => {
      res.json(model.drive);
    });

    router.put('/ebrake', (req, res) => {
      if (model.drive.ebrake) {
        model.drive.ebrake = false;
        model.drive.speed[0] = model.drive.speed[1] = 0;
        model.drive.pivot = 0;
      } else {
        model.drive.ebrake = true;
        model.drive.speed[0] = model.drive.speed[1] = 0;
        model.drive.pivot = 0;
      }
      res.json(model.drive);
    });

    // // start the tcp connection
    // router.get('/tcp', (req, res) => {
    //   connectViaTCP();
    //   res.json(model.drive);
    // });

    // let connectViaTCP = function() {
    //   if (client) {
    //       client.destroy(); // reset the connection if applicable
    //       //model.drive.connected = false; 
    //   }
    //   console.log('--> connecting to tcp on drive arduino');
    //   client = net.connect(config.drive_port, config.drive_ip, () => {
    //       console.log('--> connected to tcp on drive arduino');
    //       model.drive.connected = true;
    //       //client.setTimeout(500); 
    //   });
    //   enableClientListeners();
    // }

    // let enableClientListeners = function(){
    //   //handling ETIMEDOUT error
    //   client.on('error', (e) => {
    //       console.log("got an error", e.code);
    //       model.drive.connected = false;
    //       if (e.code == 'ETIMEDOUT') {
    //           console.log('--> Unable to Connect/Disconnected from drive arduino');
    //           connectViaTCP();
    //       }

    //   });

    //   client.on('data', function(data) {
    //       // drive arduino never sends data back.
    //       console.log('received drive data from client');
    //   });
    // }

    clear = () => {
      port.write('0    0    0    0');
      s = port.read();
      if(s) {
        console.log(s.toString())
      }
      else {
        console.log('sent')
      }
    }

    port = new SerialPort('COM6', {
      baudRate: 38400
    }
    , err => {
      if(err) {
        console.error("Error opening serial port", err.message);
      }
      else {
        console.log("started serial port")
      }
    });

    // send the current state of the rover over tcp
    let sendState = function() {
      port.write(
        [_.padEnd(model.drive.speed[0], 5),
        _.padEnd(model.drive.speed[1], 5),
        _.padEnd(model.drive.pivot, 5),
        _.toNumber(model.drive.drive_mode)].join(''),
        err => {
          if(err) {
            console.error(err.message);
            serialConnected = false;
          }
        }
      );
      let s = port.read();
      if(s) {
        //  	console.log(s.toString())
      }
    }

    setInterval(sendState, 100); // for anything under 900, it doesn't work with baud=9600
    // setInterval(clear, 800)

    console.log('-> drive server started');
    return router;
}

module.exports = {
    init
};
