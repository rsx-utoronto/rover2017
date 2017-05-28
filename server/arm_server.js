var express = require('express');
var _ = require('lodash');
var fetch = require('fetch'); 

function init(model, config) {
	model.arm = {
		desired: {
			message: 0
		}
	}

	var router = express.Router();

	// gets arm position
	router.get('/', (req, res) => {
		res.json(model.arm);
	});

	// sets desired arm position
	router.put('/:message', (req, res) => {
		model.arm.desired = _.merge(model.arm.desired, req.params)
		res.json(model.arm)
	})

	console.log('-> arm server started');
	return router;
}

module.exports = {init};