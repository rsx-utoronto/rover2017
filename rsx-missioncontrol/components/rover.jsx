import React from 'react';
import ReactDOM from 'react-dom';
import Wheel from './wheel.jsx';
import RoverBody from './rover_body.jsx'

class RoverMain extends React.Component {
	
	constructor(props) {
		super(props);
		this.state = {
			drive: {
				speed: [5,5],
				pivot: 500,
				drive_mode: true, // drive mode vs pivot mode
				temperatures: [5, 0, 0, 0, 0, 0],
				currents: [0, 0, 5, 0, 0, 0]
			}
		};
	}

	updateData() {
		fetch('http://localhost:8080/drive').then((response) => {
			if(response.ok){
				response.json().then((myJSON) => { 
					this.setState({
						drive: myJSON
					});
				});
			}
			else {
				console.log("Network Response Not OK");
			}

		})
		.catch((error) => {
			console.log("Cannot Reach Server")
		});
	}

	componentDidMount() {
		this.interval = setInterval(() => this.updateData(), 1000);
	}

	render() {
		return(
			<div className = "row text-center">
				<div className = "col-md-4 col-sm-4 col-xs-4">
					<h1>{this.state.drive.speed[0]}</h1>
					<Wheel id={0} current={this.state.drive.currents[0]} temperature={this.state.drive.temperatures[0]}/>
					<Wheel id={1} current={this.state.drive.currents[1]} temperature={this.state.drive.temperatures[1]}/>
					<Wheel id={2} current={this.state.drive.currents[2]} temperature={this.state.drive.temperatures[2]}/>
				</div>
				<div className = "col-md-4 col-sm-4 col-xs-4">
					<RoverBody pivot = {this.state.drive.pivot} drive_mode = {this.state.drive.drive_mode}/>
				</div>
				<div className = "col-md-4 col-sm-4 col-xs-4">
					<h1>{this.state.drive.speed[1]}</h1>
					<Wheel id={3} current={this.state.drive.currents[3]} temperature={this.state.drive.temperatures[3]}/>
					<Wheel id={4} current={this.state.drive.currents[4]} temperature={this.state.drive.temperatures[4]}/>
					<Wheel id={5} current={this.state.drive.currents[5]} temperature={this.state.drive.temperatures[5]}/>
				</div>
			</div>
		); 
	}

}

ReactDOM.render(
	<RoverMain/>, 
	document.getElementById('app-container')
);