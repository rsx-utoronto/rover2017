// handles mapping with leaflet. We could use this as a react component,
// but given the amount we know about react, i'd rather keep it simple.

var position = [43.783, -79.466];
var map = L.map('map').setView(position, 13); // component with id map
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
    maxZoom: 18
}).addTo(map);

// demonstrate placement of a pin
L.marker([43.7819, -79.4655]).addTo(map);