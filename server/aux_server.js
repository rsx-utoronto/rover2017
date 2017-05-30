var express = require('express');
var net = require('net');
var _ = require('lodash');
var client = undefined;

function init(model, config) {
	model.aux = {
		temperature: [0, 0, 0, 0, 0, 0],
		current: [0, 0, 0, 0, 0, 0],
		relay: [false, false, false, false, false, false]
	}

	var router = express.Router();
	router.get('/', (req, res) => {
		if(config.verbose) {
			console.log('Auxiliary readings: ', model.aux);
		}
		res.json(model.aux);
	});

	//set the relay_ith element in relay to relay_state
	router.put('/relay/:relay_i/:relay_state',(req,res) =>	{
		model.aux.relay[parseInt(req.params.relay_i)] = (req.params.relay_state !== 'false' && req.params.relay_state !== '0');
		res.json(model.aux);
	});

	// connect to the tcp client
	router.get('/tcp', (req, res) => {
		if(client)
			client.destroy()

		console.log('--> connecting to tcp on aux arduino');
        client = net.connect(config.aux_port, config.aux_ip, () => {
            console.log('--> connected to tcp on aux arduino');
        });
        //handling ETIMEDOUT error
        client.on('error', (e) => {
            console.log(e.code);
            if (e.code == 'ETIMEDOUT') {
                console.log('--> Unable/Disconnected from drive arduino');
            }
        });

        client.on('data', function(data) {
            model.aux.current = data.toString()
            						.split(',')
            						.slice(0,-1) // remove empty elemetn at end 
            						.map(parseFloat); 
        });

        res.json(model.aux);
	})

    // send the current state of the rover over tcp
    let sendState = function() {
        if (client && client.writable) {
            client.write(model.aux.relay.map(_.toInteger).join(''));
        }
    }
    setInterval(sendState, 200);

	console.log('-> aux sensor started');
	return router;
}

module.exports = {init};
