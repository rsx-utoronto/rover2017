var express = require('express');

function init(model, config) {
	model.sensor = {
		temperature: [0, 0, 0, 0, 0, 0],
		current: [0, 0, 0, 0, 0, 0],
		humidity: 0,
		outer_temp: 0,
		gas: 0
	}

	var router = express.Router();
	router.get('/', (req, res) => {
		if(config.verbose) {
			console.log('Sensor readings:', model.sensor);
		}
		res.json({value: model.sensor});
	});

	return router;
}

module.exports = {init};