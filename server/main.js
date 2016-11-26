// command line arguments to control which systems are enabled
var _ = require('lodash');
var Promise = require('bluebird');
var program = require('commander')
	.usage('node main.js [options]')
	.option('-s, --serial', 'Enable arduinos connected over serial')
	.option('-v, --verbose', 'Enable verbose debugging')
	.parse(process.argv)
var fs = Promise.promisifyAll(require('fs'));
var cors = require('cors')
var express = require('express')
var app = express();

var driveServer = require('./drive_server');
var armServer = require('./arm_server')
var serialConnection = program.serial ? require('./serial_connection') : require('./dummy_system');

model = {
	drive: {},
	arm: {}
};

console.log('Starting server...');
fs.readFileAsync('./../config.json', 'utf8')
.then(function(configFile) {
	console.log('-> loaded config file');
	config = _.assignIn(JSON.parse(configFile), program);

	app.use(cors({
		origin: [config.dashboard_port, config.drive_port, config.arm_port].map(x => 'http://localhost:' + x)
	}));
	app
		.use('/drive/', driveServer.init(model, config))
		.use('/arm/', armServer.init(model, config))
	serialConnection.init(model, config);

	app.listen(config.server_port);
})
.catch(function(err) {
	console.error("error", err);
});

console.log('Server has started');