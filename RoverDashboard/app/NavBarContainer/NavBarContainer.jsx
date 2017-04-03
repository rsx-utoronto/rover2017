import React from 'react'
import { Navbar, Nav, NavDropdown, MenuItem, NavItem, Glyphicon } from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap'
import Logo from './logo.png';

import EBrakeComponent from './components/EBrakeComponent.jsx'

require('./stylesheets/NavBar.sass')

export default class NavBarContainer extends React.Component{

  constructor(props) {
    super(props)
  }

  render() {
    return(
      <Navbar fixedTop collapseOnSelect>
        <Navbar.Header>
          <Navbar.Brand>
            <a href="#/home">
              <img src={Logo}></img>
            </a>
          </Navbar.Brand>
          <Navbar.Toggle/>
        </Navbar.Header>
        <Navbar.Collapse>
          <Nav pullRight>
            <NavItem><EBrakeComponent/></NavItem>
            <LinkContainer to={{pathname: '/home'}}>
              <NavItem><Glyphicon glyph="home"/> Home</NavItem>
            </LinkContainer>
            <LinkContainer to={{pathname: '/science'}}>
              <NavItem><Glyphicon glyph="tasks"/> Scientific Data & Charts</NavItem>
            </LinkContainer>
            <LinkContainer to={{pathname: '/camera'}}>
              <NavItem><Glyphicon glyph="camera"/> Camera</NavItem>
            </LinkContainer>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
    )
  }
}
