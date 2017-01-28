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

	console.log('-> gps server started');
	return router;
}

module.exports = {init};