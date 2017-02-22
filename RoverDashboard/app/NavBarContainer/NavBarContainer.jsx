import React from 'react'
import { Navbar, Nav, NavDropdown, MenuItem, NavItem } from 'react-bootstrap'
import Logo from './logo.png';

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
            <a href="#">
              <img src={Logo}></img>
            </a>
          </Navbar.Brand>
          <Navbar.Toggle/>
        </Navbar.Header>
        <Navbar.Collapse>
          <Nav pullRight>
            <NavItem>Home</NavItem>
            <NavItem href="#/science">Science Charts</NavItem>
            <NavItem href="#/setup">Setup & Configurations</NavItem>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
    )
  }
}
