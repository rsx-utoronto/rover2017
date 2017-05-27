var express = require('express');
var _ = require('lodash');
var net = require('net');

const sensorNames = ['humidity', 'outer_temp', 'gas', 'sens1', 'sens2', 'sens3', 'sens4', 'sens5', 'sens6'];
var client;

function init(model, config) {
	model.science = _.assign(
		_.zipObject(sensorNames, _.fill(Array(sensorNames.length), 0)),  // {humidity: undefined, gas: undefined, ...}
		{
			carousel: 0,
			drill: 0
		}
	);

	var router = express.Router();
	router.get('/', (req, res) => {
		if(config.verbose) {
			console.log('Science readings:', model.science);
		}
		res.json(model.science);
	});

    // start the tcp connection
    router.get('/tcp', (req, res) => {
      connectViaTCP();
      res.json(model.science);
    });

    let connectViaTCP = function() {
      if (client)
          client.destroy(); // reset the connection if applicable

      console.log('--> connecting to tcp on science arduino');
      client = net.connect(config.drive_port, config.drive_ip, () => {
          console.log('--> connected to tcp on science arduino');
      });
      enableClientListeners();
    }

    let enableClientListeners = function(){
      //handling ETIMEDOUT error
      client.on('error', (e) => {
          console.log(e.code);
          if (e.code == 'ETIMEDOUT') {
              console.log('--> Unable to Connect/Disconnected from science arduino');
              connectViaTCP();
          }
      });

      client.on('data', function(data) {
          console.log('received science data from client: ');
      	  //console.log(data);
      });
    }

    // send the current state of the rover over tcp
    let sendState = function() {
        if (client && client.writable) {
        	client.write(`${model.science.carousel}${model.science.drill}`);
        }
    }
    setInterval(sendState, 200);

	console.log('-> science server started');
	return router;
}

module.exports = {init};