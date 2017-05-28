var express = require('express');
var _ = require('lodash');
var fetch = require('node-fetch'); 
var SerialPort = require('serialport')

function init(model, config) {
	model.arm = {
		desired: {
			message: 0
		}
	}

	var router = express.Router();
	var port = new SerialPort('/dev/tty-usbserial1')

	// gets arm position
	router.get('/', (req, res) => {
		res.json(model.arm);
	});

	// sets desired arm position
	router.put('/:message', (req, res) => {
		model.arm.desired = _.merge(model.arm.desired, req.params)
		res.json(model.arm)
	})

	port.on('open', function() {
  		port.write(model.arm.desired, function(err) {
    		if (err) {
      	return console.log('Error on write: ', err.message);
   		}
    	console.log('message written');
		});
	})
	// open errors will be emitted as an error event 
	port.on('error', function(err) {
  		console.log('Error: ', err.message);
	})

	console.log('-> arm server started');
	return router;
}

module.exports = {init};

