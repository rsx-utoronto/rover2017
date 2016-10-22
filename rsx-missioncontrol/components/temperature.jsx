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

	updateStatus() {
		let status;

		if(this.state.temperature <= 25){
			status = stateOk;
		}
		else if(this.state.temperature > 25 && this.state.temperature <= 45){
			status = stateDanger;
		}
		else if (this.state.temperature > 45){
			status = stateCritical;
		}

		this.setState((prevState) => ({
			temperature: prevState.temperature + 1,
			status: status
		}));
	}

	componentDidMount() {
		this.interval = setInterval(() => this.updateStatus(), 300);
	}

	render() {
		return(
			<div style = {this.state.status}>
				<p>{this.state.temperature} C</p>
			</div>
		); 
	}

}
