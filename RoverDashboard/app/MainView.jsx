import React from 'react'
import NavBarContainer from './NavBarContainer/NavBarContainer.jsx'
import HomeView from './HomeView/HomeView.jsx'

export default class MainView extends React.Component {

  constructor(props) {
    super(props)
  }

  render() {
    return(
      <div className="MainView">
        <NavBarContainer/>
        {this.props.children}
      </div>
    )
  }
}
