var $ = require('jquery')
window.jQuery = $
window.$ = $

 window.ServerAddress = "192.168.0.100"
 //window.ServerAddress = "100.64.79.183"
// window.ServerAddress = "localhost"

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/css/bootstrap-theme.css'
import './css/style.css'
import './css/c3.css'

require('bootstrap')
import React from 'react'
import ReactDOM from 'react-dom'
import MainView from './app/MainView.jsx'
import HomeView from './app/HomeView/HomeView.jsx'
import ScienceCharts from './app/Graphs/science_charts.jsx'
import Setup from './app/Setup/setup.jsx'
import NavBarContainer from './app/NavBarContainer/NavBarContainer.jsx'
import { Router, Route, Link, hashHistory, IndexRedirect} from 'react-router'
import Camera from './app/Camera/Camera.jsx'


ReactDOM.render((
  <Router history={hashHistory}>
    <Route path="/" component={MainView}>
      <IndexRedirect to="/home" />
      <Route path="/home" component={HomeView}/>
      <Route path="/science" component={ScienceCharts}/>
      <Route path="/camera" component={Camera}/>
    </Route>
  </Router>
), document.getElementById('app-container'))
