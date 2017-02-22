import React from 'react'
import { Modal, Button, OverlayTrigger, Glyphicon } from 'react-bootstrap'
import Setup from '../../Setup/setup.jsx'

export default class ConfigModal extends React.Component {

  constructor(props) {
    super(props)
    this.state = {
      showModal: this.props.showModal
    }

    this.show = this.show.bind(this)
    this.close = this.close.bind(this)
  }

  show() {
    this.setState({
      showModal: true
    })
  }
  close() {
    this.setState(
      {showModal: false}
    )
  }


  render() {
    return(
      <div>
          <Button bsStyle="info" onClick={this.show}><Glyphicon glyph="cog"/></Button>
          <Modal show={this.state.showModal} onHide={this.close}>
              <Modal.Header closeButton>
                <Modal.Title>Connection & Controller Settings</Modal.Title>
              </Modal.Header>
              <Modal.Body>
                <Setup/>
              </Modal.Body>
              <Modal.Footer>
                <Button onClick={this.close}>Close</Button>
              </Modal.Footer>
            </Modal>
      </div>

    )
  }
}
