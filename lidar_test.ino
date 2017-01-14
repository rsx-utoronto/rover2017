/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/
#include <Wire.h>
#include <LIDARLite.h>
#include <Servo.h>
LIDARLite myLidarLite;

const int SERVO_PIN1 = 9;
const int SERVO_PIN2 = 10;
const int ONE_LOW = 30;
const int ONE_HIGH = 180;
const int TWO_LOW = 40;
const int TWO_HIGH = 120;

int serial_input = 0;
int pos1 = ONE_LOW + 1;
int pos2 = TWO_LOW + 1;
int dir1 = 1;
int dir2 = 1;

Servo myservo1;  // create servo object to control a servo
Servo myservo2;
// twelve servo objects can be created on most boards

void setup() {
  Serial.begin(115200);
  myLidarLite.begin();
  myservo1.attach(SERVO_PIN1);  // attaches the servo on pin 9 to the servo object
  myservo2.attach(SERVO_PIN2);
}

void loop() {
  
  if (pos1 <= ONE_LOW || pos1 >= ONE_HIGH) {
    dir1 *= -1;
  }
  if (pos2 <= TWO_LOW || pos2 >= TWO_HIGH) {
    dir2 *= -1;
  }
  pos1 += dir1;
  pos2 += dir2;
  myservo1.write(pos1);
  myservo2.write(110);
  //String result = myLidarLite.distance(); 
  Serial.println(String(pos1) + "   " + String(pos2) + "   " + myLidarLite.distance());
  delay(5);

}
