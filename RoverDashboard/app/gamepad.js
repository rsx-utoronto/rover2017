var haveEvents = 'ongamepadconnected' in window;
var controller = null;

function connecthandler(e) {
  addgamepad(e.gamepad);
}

function addgamepad(gamepad) {
  controller = gamepad;
  requestAnimationFrame(updateStatus);
}

function disconnecthandler(e) {
  controller = null;
}

function updateStatus() {
  if (!haveEvents) {
    scangamepads();
  }
  requestAnimationFrame(updateStatus);
}

function scangamepads() {
  var gamepads = navigator.getGamepads ? navigator.getGamepads() : (navigator.webkitGetGamepads ? navigator.webkitGetGamepads() : []);

  var activeGamepad = 2;
  if (gamepads[activeGamepad]) {
	  controller = gamepads[activeGamepad];

    fbSpeed = Math.floor(gamepads[activeGamepad].axes[1] * -100); // rover is too fast rn
    pivotSpeed = Math.floor(gamepads[activeGamepad].axes[5] * 100);
    console.log('game controller', fbSpeed, pivotSpeed, gamepads[2].axes)

    if(Math.abs(fbSpeed) < 10 && Math.abs(pivotSpeed) < 10) {
      fetch("http://" + ServerAddress + ":8080/drive/stop", {
        method: 'put'
      })
    }
    if(Math.abs(fbSpeed) > Math.abs(pivotSpeed))
      fetch("http://"+ServerAddress+":8080/drive/speed/"+fbSpeed+"/",{
        method: 'put'
      });
    else {
      fetch("http://"+ServerAddress+":8080/drive/pivot/"+pivotSpeed+"/", {
        method: 'put'
      });
    }
  }
}

console.log("Running scriptExample.js");
window.addEventListener("gamepadconnected", connecthandler);
window.addEventListener("gamepaddisconnected", disconnecthandler);

var speed = 100;

// key listeners
window.onkeyup = function(e) {
  let key = e.keyCode;

  if(key == 38) {  // up key
  	console.log('speed to ', speed)
    fetch("http://"+ServerAddress+":8080/drive/speed/"+(speed)+"/",{
      method: 'put'
    });
  }
  else if (key == 40) { // down key
   fetch("http://"+ServerAddress+":8080/drive/speed/"+(-speed)+"/",{
      method: 'put'
    });
  }
  else if(key == 37) {  // left key
    fetch("http://"+ServerAddress+":8080/drive/pivot/"+(speed)+"/",{
      method: 'put'
    });
  }
  else if (key == 39) { // down key
   fetch("http://"+ServerAddress+":8080/drive/pivot/"+(-speed)+"/",{
      method: 'put'
    });
  }

  // speed control
  if (key == 73) { // page down
    speed -= 10;
    speed = Math.max(speed, 0);
    console.log("speed is", speed)
  }
  else if (key == 85) { // page up
    speed += 10;
    speed = Math.min(speed, 255);
    console.log("speed is", speed)
  }
}

if (controller == null) {
  setInterval(scangamepads, 100);
}
