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

  activeGamepad = 2;
  if (gamepads[activeGamepad]) {
	  controller = gamepads[activeGamepad];

    fbSpeed = Math.floor(gamepads[activeGamepad].axes[1] * -255);
    pivotSpeed = Math.floor(gamepads[activeGamepad].axes[5] * -255);
    // console.log('game controller', fbSpeed, pivotSpeed, gamepads[2].axes)

    if(Math.abs(fbSpeed) > Math.abs(pivotSpeed))
      fetch("http://localhost:8080/drive/speed/"+fbSpeed+"/",{
        method: 'put'
      });
    else {
      fetch("http://localhost:8080/drive/pivot/"+pivotSpeed+"/", {
        method: 'put'
      });
    }
  }
}

console.log("Running scriptExample.js");
window.addEventListener("gamepadconnected", connecthandler);
window.addEventListener("gamepaddisconnected", disconnecthandler);

if (controller == null) {
  setInterval(scangamepads, 50);
}

