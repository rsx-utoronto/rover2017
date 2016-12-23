// command line arguments to control which systems are enabled
var _ = require('lodash');
var Promise = require('bluebird');
var program = require('commander')
	.usage('node main.js [options]')
	.option('-d, --drive-arduino', 'Enable drive arduino connected over serial')
	.option('-a, --arm-arduino', 'Enable arm arduino connected over serial')
	.option('-x, --aux-arduino', 'Enable auxiliary sensor arduino connected over serial')
	.option('-s, --science-arduino', 'Enable science sensor arduino connected over serial')
	.option('--all-arduinos', 'Enable all arduinos')
	.option('-v, --verbose', 'Enable verbose debugging')
	.parse(process.argv)
var fs = Promise.promisifyAll(require('fs'));
var cors = require('cors')
var express = require('express')
var app = express();

var driveServer = require('./drive_server');
var armServer = require('./arm_server')
var scienceServer = require('./science_server');
var auxServer = require('./aux_server');
var driveSerial = program.driveArduino || program.allArduinos ? require('./drive_serial') : require('./dummy_system');

if(program.armArduino || program.auxArduino || program.scienceArduino) {
	console.warn("Serial connections have not all been implemented yet :(")
}

model = {
	drive: {},
	arm: {},
	science: {},
	aux: {}
};

console.log('Starting server...');
fs.readFileAsync('./../config.json', 'utf8')

new Promise((resolve, reject) => {
	// Resolve with the first of the files below that exists
	return Promise.mapSeries(
		['./config.json', '../config.json', './example_config.json', '../example_config.json']
		, (filename) => fs.readFileAsync(filename, 'utf-8')
		.then(file => {
			resolve([filename, file]);
			return true;
		})
		.catch(_.stubFalse)
	)
	.then(files => { // this is required to reject when we don't receive any files
		if(!files.some(x => x))
			reject('did not receive any files');
	});
})
.then(function([filename, configFile]) {
	console.log(`-> loaded config file from ${filename}`);
	config = _.assignIn(JSON.parse(configFile), program);

	app.use(
		cors({origin: [config.dashboard_port, config.drive_port, config.arm_port, config.sensor_port, config.aux_port]
			.map(x => 'http://localhost:' + x)}))
	.use('/drive/', driveServer.init(model, config))
	.use('/arm/', armServer.init(model, config))
	.use('/science/', scienceServer.init(model, config))
	.use('/aux/', auxServer.init(model, config))

	driveSerial.init(model, config);

	app.listen(config.server_port);
})
.catch(function(err) {
	console.error("error", err);
});

console.log('Server has started');