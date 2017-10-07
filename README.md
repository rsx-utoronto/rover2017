# RSX Rover 2017
- React frontend
- Express backend
- Connection to Arduino

### Running the full toolkit
Navigate to the folder where you want to install everything
- ` $ git clone --recursive https://github.com/rsx-utoronto/rover `
- ` $ cd rover `

##### Installing Front-end
- ` $ cd RoverDashboard `
- ` $ npm install `

##### Running Front-end
- ` $ npm start`
- Navigate to localhost:3000 in your browser

##### Installing Server
In a new window
- ` $ npm install `

##### Running Server
- ` $ cd server `
- ` $ node main.js # runs the server `
Can also use `nodemon main.js` for hot reloading.

### Starting Drive
- Connect computer to the router
- Run the front-end and server.
- Click on the gear
- Hit connect for the drive arduino
- Select drive for the relevant joystick

### Server Command line arguments
- `-h` enables help
- `-all-arduinos` enables all the arduinos on serial ports. see `main.js` for how to enable specific systems
- `-v` enables verbose debugging
- `-l` enables the lidar

### Installing lidar
- Lidar should be installed in the `server/lib` folder:
`cd server/lib
- Lidar repo can be installed with `git submodule update --init --recursive`
- Lidar repo can be updated with `git submodule update --recursive` (haven't tried this yet)

Notes:
- You can copy `example_config.json` to `config.json` if you need to set your own settings. The latter will have a higher priority.