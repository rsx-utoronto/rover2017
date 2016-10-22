// command line arguments to control which systems are enabled
var program = require('commander')
	.usage('node main.js [options]')
	.option('-s, --serial', 'Enable arduinos connected over serial');
var promise = require('bluebird');
var fs = promise.promisifyAll(require('fs'));


var drive = require('./drive_server');
// var system = program.serial ? require('./serial_connection') : require('./dummy_system');

model = {
	drive: {
		speed: [0, 0],
		pivot: 0,
		drive_mode: true, // drive mode vs pivot mode
		temperatures: [0, 0, 0, 0, 0, 0],
		currents: [0, 0, 0, 0, 0, 0]
	}
};

fs.readFileAsync('./../config.json', 'utf8')
.then(function(config) {
	config = JSON.parse(config);
	drive.init(model, config);
})
.catch(function(err) {
	console.error(err);
});

console.log('done');