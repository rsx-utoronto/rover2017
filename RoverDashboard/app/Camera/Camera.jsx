import React from 'react'
import { Grid, Row, Col } from 'react-bootstrap'

export default class Camera extends React.Component {

  constructor(props) {
    super(props)
  }

  render() {
    return(
      <Grid>
        <Row>
          <Col md={12}>
            <img src="http://192.168.0.102/videostream.cgi?user=rsx&pwd="/>
          </Col>
        </Row>
      </Grid>
    )
  }
}
