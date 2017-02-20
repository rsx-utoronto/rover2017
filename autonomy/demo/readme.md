# Demo

## Contents

- demo.py: the main demo code
- LidarBuffer.py: contains the LidarBuffer class, which continously reads data from the lidar and stores it in a buffer, which can be read from in the main program
- TestRoverWheels.py: contains the Rover class, which is used to send drive commands to the rover (the requests commands are untested)
- transforms.py: functions for coordinate transformations, only used to transform from spherical to rectangular for the demo
- lidar.ino: the arduino code needed to communicate with the lidar

## Dependencies

- numpy
- requests

## Setup

### Connections

                                                   wheels
                                                    |
                                                    V
    laptop (server and python) ----> router ----> arduino <---- lidar
                    ^           wifi       ethernet   |
                    |                                 |
                    -----------------------------------
                                  serial

### Procedure

1. Make the connections as in the diagram (lidar lite wiring [here](https://github.com/PulsedLight3D/LIDARLite_v2_Arduino_Library#pwm-wiring); capacitor ~680μF, not strictly necessary)
2. Start the server on the laptop, and connect to the arduino with drive/tcp
3. Run the demo code