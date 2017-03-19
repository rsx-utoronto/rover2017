/*
Server for the GPS

- Install the GPSLogger App for Android
- Run the node server
- Set the app to log to *your IP address*:8080/gps/log?lat=%LAT&lon=%LON&time=%TIME
-> ([Hamburger button] > Logging details > Enable log to custom URL, and set the fields)
- Start data collection
-> You can check if the server is receiving data by running it with the --verbose option
-> You can also check if the data is being sent by going to the Log view
-> You may want to play with the frequency of sending data. For now, it's not that accurate
*/

var express = require('express');

function init(model, config) {
	model.gps = config.initial_position;

	var router = express.Router();
	router.get('/', (req, res) => {
		if(config.verbose) {
			console.log('GPS readings: ', model.gps);
		}
		res.json(model.gps);
	});

	router.get('/log', (req, res) => {
		// we can implement filtering/ sensor fusion later
		model.gps.latitude = req.query.lat || req.query.latitude;
		model.gps.longitude = req.query.lon || req.query.longitude;
		model.gps.time = req.query.time;

		if (config.verbose)
			console.log("Updating GPS coordinates: ", model.gps);

		res.json(model.gps);
	})

	console.log('-> gps server started');
	return router;
}

module.exports = {init};