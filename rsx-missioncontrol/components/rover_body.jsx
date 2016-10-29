import React from 'react';

export default class RoverBody extends React.Component{

	constructor(props){
		super(props);
		this.state = {
			pivot : this.props.pivot,
			drive_mode : this.props.drive_mode
		};
	}

	componentWillReceiveProps(newProps) {
		this.setState({
			pivot: newProps.pivot,
			drive_mode: newProps.drive_mode
		});
	}

	render() {
		return(
			<div className = "rover-body container-fluid">
				<div className = "row">
					{this.state.pivot}
				</div>
				<div className = "row">
					Drive Mode : {String(this.state.drive_mode)}
				</div>
			</div>
		);
	}
}