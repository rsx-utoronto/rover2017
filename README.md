# RSX Rover 2017
- React frontend
- Express backend
- Connection to Arduino

### Running the full toolkit
##### General
- ` $ npm install `
- ` $ npm install -g http-server `
- ` $ npm install -g webpack `
##### Frontend window
- ` $ cd rsx-missioncontrol && webpack webpack.config.js bundle.js # compile the frontend `
- ` $ http-server -p 3000  # runs the frontend `
##### Server window
` $ cd server && node main.js # runs the server `

### Command line arguments
- `-h` enables help
- `-all-arduinos` enables all the arduinos on serial ports. see `main.js` for how to enable specific systems
- `-v` enables verbose debugging

Notes:
- You can copy `example_config.json` to `config.json` if you need to set your own settings. The latter will have a higher priority.