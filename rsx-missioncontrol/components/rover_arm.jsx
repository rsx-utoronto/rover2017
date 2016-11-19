import React from "react";
import ReactDOM from "react-dom";

export default class RoverArm extends React.Component {

	constructor(props) {
		super(props)
	}

	render() {
		return(
			<div className="embed-responsive embed-responsive-16by9">
				<iframe src="//giphy.com/embed/v4sOCVX9Dhsv6" width="480" height="270" frameBorder="0" className="giphy-embed"></iframe>
			</div>
		);
	}
}

