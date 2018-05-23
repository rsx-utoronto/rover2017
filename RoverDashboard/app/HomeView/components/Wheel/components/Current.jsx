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

	componentWillReceiveProps(newProps) {
		let status;

		if(newProps.current <= 10){
			status = stateOk;
		}
		else if(newProps.current > 10 && newProps.current <= 20){
			status = stateDanger;
		}
		else if (newProps.current > 20){
			status = stateCritical;
		}

		this.setState((prevState) => ({
			current: newProps.current,
			status: status
		}));
	}

	componentDidMount() {
		
	}

	render() {
		return(
			<div style = {this.state.status}>
				<p >{this.state.current} mA</p>
			</div>
		); 
	}

}
