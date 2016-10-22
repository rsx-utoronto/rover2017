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

export default class Current extends React.Component {
	
	constructor(props) {
		super(props);
		this.state = {
			current: this.props.current,
			status: stateOk //ok, danger, critical 
		};
	}

	updateStatus() {
		let status;

		if(this.state.current <= 10){
			status = stateOk;
		}
		else if(this.state.current > 10 && this.state.current <= 20){
			status = stateDanger;
		}
		else if (this.state.current > 20){
			status = stateCritical;
		}

		this.setState((prevState) => ({
			current: prevState.current + 1,
			status: status
		}));
	}

	componentDidMount() {
		this.interval = setInterval(() => this.updateStatus(), 700);
	}

	render() {
		return(
			<div style = {this.state.status}>
				<p >{this.state.current} mA</p>
			</div>
		); 
	}

}
