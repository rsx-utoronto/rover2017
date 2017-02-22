var express = require('express');

function init(model, config) {
	model.aux = {
		temperature: [0, 0, 0, 0, 0, 0],
		current: [0, 0, 0, 0, 0, 0],
		relay: [false, false, false, false, false, false]
	}

	var router = express.Router();
	router.get('/', (req, res) => {
		if(config.verbose) {
			console.log('Auxiliary readings: ', model.aux);
		}
		res.json(model.aux);
	});

	//set the relay_ith element in relay to relay_state
	router.put('/relay/:relay_i/:relay_state',(req,res) =>	{
		model.aux.relay[parseInt(req.params.relay_i)] = (req.params.relay_state !== 'false' && req.params.relay_state !== '0');
		res.json(model.aux.relay[parseInt(req.params.relay_i)]);
	});

	console.log('-> aux sensor started');
	return router;
}

module.exports = {init};
