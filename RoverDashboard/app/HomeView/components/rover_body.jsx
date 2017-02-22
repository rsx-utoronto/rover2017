import React from 'react';
import { ListGroup, ListGroupItem } from 'react-bootstrap'

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
			<ListGroup>
				<ListGroupItem>Pivot : {this.state.pivot}</ListGroupItem>
				<ListGroupItem>Drive Mode : {String(this.state.drive_mode)}</ListGroupItem>
			</ListGroup>
		);
	}
}
