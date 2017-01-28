import React from 'react';

export default class RoverLocation extends React.Component {

	constructor(props) {
		super(props);
	}

	render() {
		return(
			<div className="col-md-9 offset-md-2">
				<img className = "img-responsive center-block" src="mars_map.png" />
			</div>
		);
	}
}