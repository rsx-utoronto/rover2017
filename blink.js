var SerialPort = require('serialport');

var port = new SerialPort('COM6', {
  baudRate: 9600
});


clear = () => port.write('0    0    0    0');

set = () => port.write('123  123  123  1');
flag = false;

setInterval(function() {
	if(flag) {
		clear();
	}
	else {
		set();
	}
	flag = !flag;
}, 500);
