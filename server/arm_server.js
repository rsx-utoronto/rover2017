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
	var port = new SerialPort('/dev/tty-usbserial1');
	var portOpen = false; 

	port.on('open', function() {
		portOpen = true; 
	})

	// gets arm position
	router.get('/', (req, res) => {
		res.json(model.arm);
	});

	// sets desired arm position
	router.put('/:message', (req, res) => {
		model.arm.desired = _.merge(model.arm.desired, req.params)
		res.json(model.arm);

		if (portOpen)
			port.write(model.arm.desired.message, (err) => {
				if (err) { 
					console.error("Serial port didn't write correctly"); 
				}
				else { 
					console.log("Serial port written"); 
				}
			})
	})

	

	console.log('-> arm server started');
	return router;
}

module.exports = {init};

