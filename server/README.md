# Server Documentation
The server is broken up into several endpoints that you can use to read information about the rover and write commands to it. The basic format of a request for information is:

`GET {ip address of the rover}/{system}`
e.g. `GET 123.123.123.123/drive/`

The basic format of a command to the server is:

`PUT {ip address of the rover}/{system}/{function}/{variable1}/{variable2}/{...}`
e.g. `PUT 123.123.123.123/drive/pivot/30`


## Specific Systems
### Drive System: `/drive`
The drive system controls the drive motors on the rover. There are two modes: drive and pivot. The first lets the rover move straight and do gentle curves. The second lets the rover turn on the spot. These are different because of how the rocker bogie works. The variable `drive_mode` controls which of the two modes is used.

The endpoints are:
`GET /`: Gets the drive state. All PUT queries will also return this information. The information is in the form: ``` {
	speed: [int, int], pivot: int, drive_mode: boolean
}```

`PUT /speed/{speed}`: Sets the speed of both motors. Returns the drive state.

`PUT /speed/{left speed}/{right speed}`: Individually sets the speeds of the motors. Returns the drive state

`PUT /pivot/{pivot speed}`: Sets the rover to pivot on the spot. Returns the drive state.

`PUT /stop`: Stops the rover. Returns the drive state.


### Arm System: `/arm`
tbd

### Auxiliary System:
The auxiliary system reports the state of the temperature and current sensors, as well as the relays.

Endpoint:
`GET /`: Gets the auxiliary state. The information is in the form: ``` {
	temperature: [float * 6], current: [float * 6], aux: [boolean * 6]
}```

`PUT /relay/{relay_index}/{relay_state}`: Sets the state of the i'th relay. `relay_state` can be `true` or `1` for truthy values, and `false` or `0` as falsy values. Returns the aux state.

### Science System:
The science system reports the state from the science sensors.

Endpoint:
`GET /`: Gets science state. The format has not been determined yet.