import React from 'react'
import ReactDOM from 'react-dom'
import { Panel, Grid, Row, Col, Table, Button } from 'react-bootstrap'
import Wheel from './components/Wheel/Wheel.jsx'
import RoverBody from './components/rover_body.jsx'
import Speed from './components/speed.jsx'
import RoverArm from './components/rover_arm.jsx'
import Map from './components/Map.jsx'
import KeepAlive from '../KeepAlive/KeepAlive.jsx'
import ConfigModal from './components/ConfigModal.jsx'

require('./stylesheets/HomeView.sass')

const RoverStatusPanel = (
	<div className="RoverStatusPanelTitle">
		<h4>Rover Info</h4>
		<ConfigModal/>
	</div>
)


export default class HomeView extends React.Component {

	constructor(props) {
		super(props)
		this.state = {
			drive: {
				speed: [5,5],
				pivot: 500,
				drive_mode: true,
				connected: false
			},
			aux: {
				current: [0, 0, 0, 0, 0, 0],
				relay: [false, false, false, false, false, false],
				temperature: [0, 0, 0, 0, 0, 0]
			}
		}
	}

	updateData() {
		fetch("http://"+ServerAddress+":8080/drive").then((response) => {
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

		fetch("http://"+ServerAddress+":8080/aux").then((response) => {
			if(response.ok){
				response.json().then((myJSON) => {
					this.setState({
						aux: myJSON
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
		this.interval = setInterval(() => this.updateData(), 500)
	}
	componentWillUnmount() {
		clearInterval(this.interval)
	}

	render() {
		let wheel = [0,1,2,3,4,5]
		wheel = wheel.map((i) =>
			<Wheel key={i}
						 index={i}
						 current={this.state.aux.current[i]}
						 temperature={this.state.aux.temperature[i]}
						 relay={this.state.aux.relay[i]}
			/>
		)

		return(
			<div className="ViewContainer">
				<Map />
				<Panel className="panelTest" header={RoverStatusPanel} >
					<Table bordered>
				    <thead>
				      <tr>
				        <th>Left</th>
				        <th>Right</th>
				      </tr>
				    </thead>
				    <tbody>
				      <tr>
								<td><Col md={3}>{wheel[0]}</Col></td>
								<td><Col md={3}>{wheel[3]}</Col></td>
				      </tr>
				      <tr>
				        <td><Col md={3}>{wheel[1]}</Col></td>
				        <td><Col md={3}>{wheel[4]}</Col></td>
				      </tr>
							<tr>
				        <td><Col md={3}>{wheel[2]}</Col></td>
				        <td><Col md={3}>{wheel[5]}</Col></td>
				      </tr>
				    </tbody>
				  </Table>
					<RoverBody pivot = {this.state.drive.pivot} drive_mode = {this.state.drive.drive_mode} connected = {this.state.drive.connected}/>
				</Panel>
			</div>
		)
	}

}
