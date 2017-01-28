import React from 'react';
import {LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend} from 'Recharts';

const data = [
      {name: 'Page A', uv: 4000, pv: 2400, amt: 2400},
      {name: 'Page B', uv: 3000, pv: 1398, amt: 2210},
      {name: 'Page C', uv: 2000, pv: 9800, amt: 2290},
      {name: 'Page D', uv: 2780, pv: 3908, amt: 2000},
      {name: 'Page E', uv: 1890, pv: 4800, amt: 2181},
      {name: 'Page F', uv: 2390, pv: 3800, amt: 2500},
      {name: 'Page G', uv: 3490, pv: 4300, amt: 2100},
];

class SimpleLineChart extends React.Component {

	constructor(props) {
		super(props);
	}

	render () {
	  	return (
	    	<LineChart width={400} height={300} data={data}
	            margin={{top: 5, right: 30, left: 20, bottom: 5}}>
	       <XAxis dataKey="name"/>
	       <YAxis/>
	       <CartesianGrid strokeDasharray="3 3"/>
	       <Tooltip/>
	       <Legend />
	       <Line type="monotone" dataKey="pv" stroke="#8884d8" activeDot={{r: 8}}/>
	       <Line type="monotone" dataKey="uv" stroke="#82ca9d" />
	      </LineChart>
	    );
  	}
}


export default class ScienceCharts extends React.Component {

	constructor(props) {
		super(props);
	}

	render() {
		return(
			<div className="row col-md-12">
		        <ul className="nav nav-tabs">
		          <li className="active"><a href="#moisture" data-toggle="tab" aria-expanded="true">Moisture</a></li>
		          <li className=""><a href="#temp" data-toggle="tab" aria-expanded="false">Temperature</a></li>
		          <li className=""><a href="#airpressure" data-toggle="tab" aria-expanded="false">Air Pressure</a></li>
		        </ul>
		        <div id="myTabContent" className="tab-content">
		          <div className="tab-pane fade active in" id="moisture">
		            <br></br>
		          	<SimpleLineChart/>
		          </div>
		          
		        </div>
		      </div>
		);
	}
}