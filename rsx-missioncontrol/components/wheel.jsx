import React from 'react';
import Temperature  from './temperature.jsx'; 
import Current  from './current.jsx'; 

export default class Wheel extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			current: this.props.current,
			temperature: this.props.temperature
		};
	}

	componentWillReceiveProps(newProps) {
		this.setState({
			current: this.props.current,
			temperature: this.props.temperature
		});
	}

	render() {
		return(
			<div className = "wheel container-fluid">
				<Temperature temp={this.state.temperature}/>
				<Current current={this.state.current}/>
			</div>

		);
	}
}