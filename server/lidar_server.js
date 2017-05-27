// Lidar server
// This server is guarded behind the -l flag because it 
// requires a lidar device to run properly. 

var _ = require('lodash');
var express = require('express');
var sweepjs = require('./lib/sweep-sdk/sweepjs/')

var sweep; 

function startLidar(port) { 
	sweep = new sweepjs.Sweep(port); 
	sweep.startScanning(); 
	if (config.verbose) {
		console.log("Starting lidar"); 
	}
}

function init(model, config) { 
	startLidar(model.lidar_port); 
	model.lidar = _.zipObject(_.range(-30, 30), new Array(60).fill(0))

	var router = express.Router(); 
	router.get('/', (req, res) => { 
		if(config.verbose) { 
			console.log('lidar readings: ', model.lidar); 
		}
		res.json(model.lidar); 
	}); 

	// restarts the lidar 
	router.get('/start', (req, res) => {
		sweep.reset(); 
		startLidar(model.lidar_port); 
	}); 

	if (config.lidar) {
		setInterval(update, 500); 
	}

	return router; 
}

function update(model) { 
	sweep.scan((err, samples) => { 
		if (err) {
			return; 
		}

		_.assign(model.lidar, 
			_(samples)
			.map(sample => [sample.angle, sample.distance])
			.fromPairs()  // {sample.angle: sample.distance for sample in samples}
		); 
	})
}

module.exports = { init }; 