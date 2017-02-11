import React from 'react'
import ReactDOM from 'react-dom'
import Wheel from './wheel.jsx'
import RoverBody from './rover_body.jsx'
import Speed from './speed.jsx'
import RoverArm from './rover_arm.jsx'
import ScienceCharts from './science_charts.jsx'
import Setup from './setup.jsx'
import Map from './Map.jsx'
import KeepAlive from './KeepAlive/KeepAlive.jsx'
import { Router, Route, Link, hashHistory} from 'react-router'


class RoverMain extends React.Component {

	constructor(props) {
		super(props)
		this.state = {
			drive: {
				speed: [5,5],
				pivot: 500,
				drive_mode: true // drive mode vs pivot mode
				// temperatures: [5, 0, 0, 0, 0, 0],
				// currents: [0, 0, 5, 0, 0, 0]
			},
			aux: {
				temperatures: [1, 0, 0, 0, 0, 0],
				currents: [1, 0, 0, 0, 0, 0]
			}
		}
	}

	updateData() {
		fetch('http://localhost:8080/drive').then((response) => {
			if(response.ok){
				response.json().then((myJSON) => {
					this.setState({
						drive: myJSON
					})
				})
			}
			else {
				console.log("Network Response Not OK")
			}

		})
		.catch((error) => {
			console.log("Cannot Reach Server")
		})
	}

	componentDidMount() {
		this.interval = setInterval(() => this.updateData(), 100)
	}
	componentWillUnmount() {
		clearInterval(this.interval)
	}

	render() {
		return(

			<div>
				<div className="row">
					<div className="col-md-12">
						<div className="panel panel-info">
							<div className="panel-heading">
								<h3 className="panel-title">Rover Location</h3>
							</div>
							<div className="panel-body">
								<KeepAlive />
								<Map />
							</div>
						</div>
					</div>
				</div>
				<div className="row">
					<div className="col-md-6">
						<div className="panel panel-info">
							<div className="panel-heading">
								<h3 className="panel-title">Rover Info</h3>
							</div>
							<div className="panel-body">
								<div className = "row">
									<div className = "col-md-3 text-center">
										<Wheel id={0} current={this.state.aux.currents[0]} temperature={this.state.aux.temperatures[0]}/>
										<Wheel id={1} current={this.state.aux.currents[1]} temperature={this.state.aux.temperatures[1]}/>
										<Wheel id={2} current={this.state.aux.currents[2]} temperature={this.state.aux.temperatures[2]}/>
									</div>
									<div className = "col-md-6 rover-body ">
										<RoverBody pivot = {this.state.drive.pivot} drive_mode = {this.state.drive.drive_mode}/>
									</div>
									<div className = "col-md-3 text-center">
										<Wheel id={3} current={this.state.aux.currents[3]} temperature={this.state.aux.temperatures[3]}/>
										<Wheel id={4} current={this.state.aux.currents[4]} temperature={this.state.aux.temperatures[4]}/>
										<Wheel id={5} current={this.state.aux.currents[5]} temperature={this.state.aux.temperatures[5]}/>
									</div>
								</div>
							</div>
						</div>
					</div>
					<div className='col-md-6'>
						<div className="panel panel-info">
							<div className="panel-heading">
								<h3 className="panel-title">Rover Arm</h3>
							</div>
							<div className="panel-body">
								<RoverArm/>
							</div>
						</div>
					</div>
				</div>
			</div>



		)
	}

}

ReactDOM.render((
  <Router history={hashHistory}>
    <Route path="/" component={RoverMain}/>
    <Route path="/science" component={ScienceCharts}/>
    <Route path="/setup" component={Setup}/>
  </Router>
), document.getElementById('app-container'))
