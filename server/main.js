// command line arguments to control which systems are enabled
var _ = require('lodash');
var Promise = require('bluebird');
var program = require('commander')
	.usage('node main.js [options]')
	.option('-s, --serial', 'Enable arduinos connected over serial')
	.option('-v, --verbose', 'Enable verbose debugging')
	.parse(process.argv)
var fs = Promise.promisifyAll(require('fs'));

var driveServer = require('./drive_server');
var serialConnection = program.serial ? require('./serial_connection') : require('./dummy_system');

model = {
	drive: {
		speed: [0, 0],
		pivot: 0,
		drive_mode: true, // drive mode vs pivot mode
		temperatures: [0, 0, 0, 0, 0, 0],
		currents: [0, 0, 0, 0, 0, 0]
	}
};

console.log('Starting server...');
fs.readFileAsync('./../config.json', 'utf8')
.then(function(configFile) {
	console.log('-> loaded config file');
	config = _.assignIn(JSON.parse(configFile), program);
	driveServer.init(model, config);
	serialConnection.init(model, config);
})
.catch(function(err) {
	console.error(err);
});

console.log('Server has started');