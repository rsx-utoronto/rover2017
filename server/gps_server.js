var express = require('express');

function init(model, config) {
	model.gps = config.initial_position;

	var router = express.Router();
	router.get('/', (req, res) => {
		if(config.verbose) {
			console.log('GPS readings: ', model.gps);
		}
		res.json(model.gps);
	});

	router.get('/log', (req, res) => {
		// we can implement filtering/ sensor fusion later
		model.gps.latitude = req.query.lat || req.query.latitude;
		model.gps.longitude = req.query.lon || req.query.longitude;
		model.gps.time = req.query.time;

		if (config.verbose)
			console.log("Updating GPS coordinates: ", model.gps);

		res.json(model.gps);
	})

	console.log('-> gps server started');
	return router;
}

module.exports = {init};