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
			<div className = "container-fluid">
				<div className = "row">
					<div className = "col-md-12">
						<ul className="list-group">
						  <li className="list-group-item">
						    <span className="badge">{this.state.pivot}</span>
						    Pivot
						  </li>
						  <li className="list-group-item">
						    <span className="badge">{String(this.state.drive_mode)}</span>
						    Drive Mode
						  </li>
						  <li className="list-group-item">
						    <span className="badge">78%</span>
						    Battery Life
						  </li>
						  <li className="list-group-item">
						    <span className="badge">-10 db</span>
						    Signal 
						  </li>
						</ul>
					</div>
				</div>
			</div>
		);
	}
}