var express = require('express');
var _ = require('lodash');

function init(model, config) {
	model.arm = {
		desired: {
			x: 0, y: 0, z: 0,
			theta1: 0, theta2: 0, theta3: 0
		},
		actual: {
			x: 0, y: 0, z: 0,
			theta1: 0, theta2: 0, theta3: 0
		}
	}

	var router = express.Router();

	// gets arm position
	router.get('/', (req, res) => {
		res.json(model.arm);
	});

	// sets desired arm position
	router.put('/position/:x/:y/:z/angle/:theta1/:theta2/:theta3', (req, res) => {
		model.arm.desired = _.merge(model.arm.desired, req.params)
		res.json(model.arm)
	})

	console.log('-> arm server started');
	return router;
}

module.exports = {init};