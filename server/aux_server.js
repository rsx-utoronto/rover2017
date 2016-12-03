var express = require('express');

function init(model, config) {
	model.aux = {
		temperature: [0, 0, 0, 0, 0, 0],
		current: [0, 0, 0, 0, 0, 0]
	}

	var router = express.Router();
	router.get('/', (req, res) => {
		if(config.verbose) {
			console.log('Auxiliary readings: ', model.aux);
		}
		res.json(model.aux);
	});

	console.log('-> aux sensor started');
	return router;
}

module.exports = {init};