var SerialPort = require("serialport");

init = function(model, config) {
	let port = new SerialPort(config.drive_com_port, {
		parser: SerialPort.parsers.readline('\n')
	},
	function (err) {
		if (err) {
			console.error(`Error: Could not start drive serial port ${config.drive_com_port}`)
			return
		}
		console.log(`-> started serial port on ${config.drive_com_port}`);
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
	});
}

module.exports = {init};