// GPS Server
// This needs to be enabled with the --gps flag on the server.
// The GPS is run from the IP webcam app, which also provides information on heading and pitch.
// https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en
// In the app's "Data Logging" tab, enable data logging, and ensure that at least battery percent
// sensor, accelerometer and magnetic field are enabled

var fetch = require('node-fetch');
var _ = require('lodash');
var express = require('express');

var phoneURL;

const SMOOTHING = 5; // number of readings to average over

function toDegrees(x) {
	return x * 180 / Math.PI;
}

function update(model) {
	// get the phone's gps coordinates
	fetch(`${phoneURL}/gps.json`)
	.then(response => response.json())
	.then(body => {
		if (body.gps.latitude)
			model.gps.latitude = body.gps.latitude;
		if (body.gps.longitude)
			model.gps.longitude = body.gps.longitude;
		if (body.gps.accuracy)
			model.gps.accuracy = body.gps.accuracy; // useful for kalman filtering
	})
	.catch(err => {
		console.error('Could not get data from gps', err);
	})

	// get the sensor readings (acceleration, heading, battery)
	fetch(`${phoneURL}/sensors.json`)
	.then(response => response.json())
	.then(body => {
		// Calculate pitch of the rover using the accelerometer, measured in degrees from horizontal.
		// Assume that the phone is in portrait mode and mounted facing forward
		// Acceleration is averaged over the last SMOOTHING iterations
		let accelHist = _(body.accel.data)
						.slice(-SMOOTHING)	// pop the last few elements
						.map(x => x[1]) 	// read data
						.unzip()			// transpose so we can calculate the mean
						.map(_.mean)
						.value()
		let accel = _.zipObject(body.accel.desc, accelHist);
		let pitchRad = Math.atan2(-accel.Az, accel.Ay); // change to y, z
		model.gps.pitch = toDegrees(pitchRad);

		let batteryLevel = _.last(body.battery_level.data)[1];  // battery level of the phone
		model.gps.battery = batteryLevel;

		// rot_vector is calculated with sensor fusion, prefer this
		if (body.rot_vector) {
			// x is pitch 
			// y is heading 
			let rotHist = _(body.rot_vector.data)
						.slice(-SMOOTHING)
						.map(x => x[1])
						.unzip()
						.map(_.mean)
						.value()
			let rot = _.zipObject(body.rot_vector.desc.map(x => x[0]), rotHist); 
			model.gps.heading = -720 * Math.asin(rot.y) / Math.PI; 
			// could probably also calculate pitch, but it requires some trig. 
		}
		else { 
			// Calculate the orientation of the rover in degrees from north.
			// Calculated as a compass bearing from north. Outputs from -180 to 180. 
			// This is calculated from the magnetometer in a similar fashion to pitch.
			let magHist = _(body.mag.data)
							.slice(-SMOOTHING)
							.map(x => x[1])
							.unzip()
							.map(_.mean)
							.value()
			let mag = _.zipObject(body.mag.desc, magHist);
			let correctedMagZ = mag.Mz * Math.cos(pitchRad) + mag.My * Math.sin(pitchRad); // apply a rotation matrix about x to correct for pitch
			model.gps.heading = toDegrees(Math.atan2(-mag.Mx, -correctedMagZ)); 
		}
	})
	.catch(err => {
		console.log("Could not get data from sensors", err)
	})
}

function init(model, config) {
	model.gps = config.initial_position;
	phoneURL = config.phone_url;
	fetch(`${phoneURL}/settings/gps_active?set=on`)
	.then(response => {
		if (response.ok){
			setInterval(() => update(model), 1000);
			console.log(`-> gps server started at ${phoneURL}`);
		}
		throw Error('gps response not okay')
	})
	.catch(err => console.error('Could not start the gps sensors'));

	// create the server interface
	var router = express.Router();
	router.get('/', (req, res) => {
		if(config.verbose) {
			console.log('GPS readings: ', model.gps);
		}
		res.json(model.gps);
	});

	// This function is provided for compatibility with the GPS logger app, which lets you write
	// to a server. The app isn't super reliable, but the code is here as a backup.
	router.get('/log', (req, res) => {
		model.gps.latitude = req.query.lat || req.query.latitude;
		model.gps.longitude = req.query.lon || req.query.longitude;
		model.gps.time = req.query.time;

		if (config.verbose)
			console.log("Updating GPS coordinates: ", model.gps);
		res.json(model.gps);
	})
	
	return router;
}

module.exports = { init };