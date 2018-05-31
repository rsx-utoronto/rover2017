var express = require('express');
var _ = require('lodash');
var fetch = require('node-fetch'); 
var SerialPort = require('serialport')

function init(model, config) {
	model.drive = {
		desired: {
			message: 0
		}
	}

	var router = express.Router();
	var port = new SerialPort('/dev/ttyUSB0', {baudRate: 9600});
	var portOpen = false; 

	port.on('open', function() {
		portOpen = true; 
	})

	// gets drive velocity
	router.get('/', (req, res) => {
		res.json(model.drive);
	});

	// sets desired drive velocity
	router.put('/:message', (req, res) => {
		model.drive.desired = _.merge(model.drive.desired, req.params)
		res.json(model.drive);

		if (portOpen)
			port.write(model.drive.desired.message, (err) => {
				if (err) { 
					console.error("Serial port didn't write correctly"); 
				}
				else { 
					console.log("Serial port written");
					console.log(model.drive.desired.message); 
				}
			})
	})

	

	console.log('-> drive server started');
	return router;
}

module.exports = {init};

