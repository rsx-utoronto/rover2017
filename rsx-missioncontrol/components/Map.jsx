import React from 'react'
import ReactDOM from 'react-dom'
import L from 'leaflet'

export default class Map extends React.Component {

	constructor(props) {
		super(props)
	}

	componentDidMount() {
		var position = [43.783, -79.466]
		var map = L.map('map').setView(position, 13) // component with id map
		L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
		    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
		    maxZoom: 18
		}).addTo(map)

		// demonstrate placement of a pin
		L.marker([43.7819, -79.4655]).addTo(map)
	}

	render() {
		return(
			<div id="map">
			</div>
		);
	}
}
