import React from 'react';
import Temperature  from './temperature.jsx'; 
import Current  from './current.jsx'; 

export default class Wheel extends React.Component {

	constructor(props) {
		super(props);
		this.state = {

		};
	}

	render() {
		return(
			<div className = "wheel container-fluid">
				<Temperature temp={7}/>
				<Current current={7}/>
			</div>

		);
	}
}