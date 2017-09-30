import React from 'react'
import Temperature  from './components/Temperature.jsx'
import Current  from './components/Current.jsx'
import MotorRelay from './components/MotorRelay.jsx'

export default class Wheel extends React.Component {

	constructor(props) {
		super(props)
		this.state = {
			index: this.props.index,
			current: this.props.current,
			temperature: this.props.temperature,
			relay: this.props.relay
		}
	}

	componentWillReceiveProps(newProps) {
		this.setState({
			current: this.props.current,
			temperature: this.props.temperature,
			relay: this.props.relay
		})
	}

	render() {
		return(
			<div>
				<Temperature temp={this.state.temperature}/>
				<Current current={this.state.current}/>
				<MotorRelay index={this.state.index} status={this.state.relay}/>
			</div>

		);
	}
}
