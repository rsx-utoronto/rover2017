var express = require('express');
var cors = require('cors');

var app = express();

function init(model, config) {
	console.log('initializing drive server')

	app.use(cors({
		origin: [config.dashboard_port, config.drive_port].map(x => 'http://localhost:' + x)
	}));
	var router = express.Router();

	// gets rover speed and turning parameters
	router.get('/', (req, res) => {
		res.json(model.drive);
	})

	// sets rover speed only. used to scale the rover speed by a factor
	router.put('/speed/:speed', (req, res) => {
		model.drive.speed = req.params.speed;
		model.drive.drive_mode = true;
		res.json(model.drive);
	});

	// sets rover speed and turning speed. used for normal driving.
	router.put('/speed/:speed/turnspeed/:turn_speed', (req, res) => {
		model.drive.speed = req.params.speed;
		model.drive.turn_speed = req.params.turn_speed;
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

	app.use('/drive', router);
	app.listen(config.server_port);
	console.log('drive server started');
}

module.exports = {init};


// question: how much computation to outsource to the Arduino vs. the server?
// arguments for arduino: modularity, ease of testing
// arguments for server: robustness, manual reconfiguration of wheels.
// i guess this isn't super important because we don't have time to do this anyways during the competition...


// todo: how to listen to multiple ports? should be able to listen to drive system and dashboard
// another slightly useful project, esp for demo: build mini-dashboards that emulate the arduinos