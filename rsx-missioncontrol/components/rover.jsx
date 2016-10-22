import React from 'react';
import ReactDOM from 'react-dom';
import Wheel from './wheel.jsx';
import RoverBody from './rover_body.jsx'

class RoverMain extends React.Component {
	
	constructor(props) {
		super(props);
		this.state = {
			drive: {
				speed: [0,0],
				pivot: 100,
				drive_mode: true, // drive mode vs pivot mode
				temperatures: [0, 0, 0, 0, 0, 0],
				currents: [0, 0, 0, 0, 0, 0]
			}
		};
	}

	updateData() {

		// fetch('node/route').then((response) => {
		// 	if(response.ok){
		// 		response.json().then((myJSON) => { 
		// 			this.setState((myJSON) => ({
		// 				drive: myJSON.drive
		// 			}));
		// 		});
		// 	}
		// 	else {
		// 		console.log("Network Response Not OK");
		// 	}

		// })
		// .catch((error) => {

		// });
	}

	componentDidMount() {
		this.interval = setInterval(() => this.updateData(), 100);
	}

	render() {
		return(
			<div className = "row text-center">
				<div className = "col-md-4 col-sm-4 col-xs-4">
					<h1>{this.state.drive.speed[0]}</h1>
					<Wheel id={0} />
					<Wheel id={1} />
					<Wheel id={2} />
				</div>
				<div className = "col-md-4 col-sm-4 col-xs-4">
					<RoverBody pivot = {this.state.drive.pivot} drive_mode = {this.state.drive.drive_mode}/>
				</div>
				<div className = "col-md-4 col-sm-4 col-xs-4">
					<h1>{this.state.drive.speed[1]}</h1>
					<Wheel id={3} />
					<Wheel id={4} />
					<Wheel id={5} />
				</div>
			</div>
		); 
	}

}

ReactDOM.render(
	<RoverMain/>, 
	document.getElementById('app-container')
);