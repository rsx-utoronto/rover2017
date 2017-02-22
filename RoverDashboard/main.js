var $ = require('jquery')
window.jQuery = $
window.$ = $

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/css/bootstrap-theme.css'
import './css/style.css'

require('bootstrap')

import React from 'react'
import ReactDOM from 'react-dom'
import HomeView from './app/HomeView/HomeView.jsx'
import ScienceCharts from './app/Graphs/science_charts.jsx'
import Setup from './app/Setup/setup.jsx'
import gamepad from './app/gamepad.js'
import NavBarContainer from './app/NavBarContainer/NavBarContainer.jsx'
import { Router, Route, Link, hashHistory} from 'react-router'

// ReactDOM.render((
//   <NavBarContainer/>
// ), document.getElementById('navbar-container'))

ReactDOM.render((
  <Router history={hashHistory}>
    <Route path="/" component={HomeView}/>
    <Route path="/science" component={ScienceCharts}/>
    <Route path="/setup" component={Setup}/>
  </Router>
), document.getElementById('app-container'))
