var SerialPort = require("serialport");
var Promise = require('bluebird');

var getSerialPorts = Promise.promisify(SerialPort.list);

init = function(model, config) {
	getSerialPorts()
	.then(portInfo => {
		let port = new SerialPort(portInfo[0].comName, {
			parser: SerialPort.parsers.readline('\n')
		});
		console.log('-> started serial port on ', portInfo[0].comName);
		if (config.verbose)
			console.log('Available ports: ', portInfo);

		port.on('data', function(data) {
			// get data from the dataport
			words = data.toString().trim().split(' ');
			newSensorValues = {}
			newSensorValues[words[0]] = words.map(x => parseFloat(x)).slice(1);
			if ('temperatures' in newSensorValues)
				model.drive.temperatures = newSensorValues.temperatures;
			if ('currents' in newSensorValues)
				model.drive.currents = newSensorValues.currents;
			driveParams = model.drive.speed.concat([model.drive.pivot, +model.drive.drive_mode]);
			port.write(driveParams.join(' ') + ' ');
			if (config.verbose)
				console.log(model.drive);
		});
	})
}

module.exports = {init};