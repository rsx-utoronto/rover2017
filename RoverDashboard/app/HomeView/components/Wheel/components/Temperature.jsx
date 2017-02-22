import React from 'react';

const stateOk = {
  color: 'black' 
};

const stateDanger = {
  color: 'orange'
};

const stateCritical = {
  color: 'red'
};

export default class Temperature extends React.Component {
	
	constructor(props) {
		super(props);
		this.state ={
			temperature: this.props.temp
		};
	}

	componentWillReceiveProps(newProps) {
		let status;

		if(newProps.temperature <= 25){
			status = stateOk;
		}
		else if(newProps.temperature > 25 && newProps.temperature <= 45){
			status = stateDanger;
		}
		else if (newProps.temperature > 45){
			status = stateCritical;
		}

		this.setState((prevState) => ({
			temperature: newProps.temp,
			status: status
		}));
	}


	componentDidMount() {
		
	}

	render() {
		return(
			<div style = {this.state.status}>
				<p>{this.state.temperature} C</p>
			</div>
		); 
	}

}
