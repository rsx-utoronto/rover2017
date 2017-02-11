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

	//get currentsensor and temperature 
	router.put('/temperature/:temperature,:current',(req,res)=>{
		model.aux.temperature=req.params.temperature;
		model.aux.current=req.params.current;
		res.json(model.aux);
	});

	//set the relay_ith element in relay to relay_state
	router.put('/relay/:relay_i/:relay_state',(req,res)=>{ 
		model.aux.relay[req.params.relay_i]=Boolean(req.params.relay_state);
		res.json(model.aux);
	});
 	
	console.log('-> aux sensor started');
	return router;
}

module.exports = {init};