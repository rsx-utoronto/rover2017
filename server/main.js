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

let filePaths = ['./config.json', '../config.json', './example_config.json', '../example_config.json'];
// Return the first config file and file name that work, see http://stackoverflow.com/questions/41307031/return-when-first-promise-resolves/
filePaths.reduce(function(promise, path) {
    return promise.catch(function(error) {
    	return fs.readFileAsync(path, 'utf-8').then(configFile => [configFile, path]);
    });
}, Promise.reject())
.then(function([configFile, filename]) {
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
	console.error("error while opening config file", err);
});

console.log('Server has started');