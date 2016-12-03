var express = require('express');

function init(model, config) {
	model.science = {
		humidity: 0,
		outer_temp: 0,
		gas: 0
	}

	var router = express.Router();
	router.get('/', (req, res) => {
		if(config.verbose) {
			console.log('Science readings:', model.science);
		}
		res.json(model.science);
	});

	console.log('-> science server started');
	return router;
}

module.exports = {init};