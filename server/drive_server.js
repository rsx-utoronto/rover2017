var express = require('express');
var cors = require('cors');

var app = express();

function init(model, config) {
	console.log('-> started drive server');

	app.use(cors({
		origin: [config.dashboard_port, config.drive_port].map(x => 'http://localhost:' + x)
	}));
	var router = express.Router();

	// gets rover speed and turning parameters
	router.get('/', (req, res) => {
		res.json(model.drive);
	})

	// sets rover forward speed.
	router.put('/speed/:speed', (req, res) => {
		model.drive.speed[0] = model.drive.speed[1] = req.params.speed;
		model.drive.drive_mode = true;
		res.json(model.drive);
	});

	// sets rover speed on both wheels.
	router.put('/speed/:speed0/:speed1', (req, res) => {
		model.drive.speed[0] = req.params.speed0;
		model.drive.speed[1] = req.params.speed1;
		model.drive.drive_mode = true;
		res.json(model.drive);
	});

	// sets the pivot speed of the rover. pivoting requires us to turn off
	// the middle wheels or the rocker bogie dies.
	router.put('/pivot/:turn_speed', (req, res) => {
		model.drive.pivot = req.params.turn_speed;
		model.drive.drive_mode = false;
		res.json(model.drive);
	});

	router.put('/stop', (req, res) => {
		model.drive.speed[0] = model.drive.speed[1] = 0;
		res.json(model.drive);
	});

	app.use('/drive', router);
	app.listen(config.server_port);
	console.log('-> drive server started');
}

module.exports = {init};