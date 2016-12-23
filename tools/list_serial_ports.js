// Get a list of connected serial ports

var Promise = require('bluebird');
var SerialPort = require("serialport");

getPortInfo = Promise.promisify(SerialPort.list);
console.log("Serial ports")
getPortInfo().then(info => console.log(info));

