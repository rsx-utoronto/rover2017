/*  Driver for the lidar light. Converts PWM from the lidar to 
 *  serial readings for use on the computer. 
 *  
 *  Setup: 
 *  Ultrasound 
 */

#include <Servo.h>

unsigned long pulse_width;
int distance = -1; 

const int SERVO_PIN1 = 6;     // left and right
// const int SERVO_PIN2 = 10;    // up and down

const int ULTRA_TRG = 2;      // ultrasonic pins
const int ULTRA_ECHO = 3; 

const int ONE_LOW = 90;       // 124 is middle
const int ONE_HIGH = 140;
const int TWO_LOW = 40;       // not used for demo
const int TWO_HIGH = 120;

int pos1 = ONE_LOW + 1;
int pos2 = TWO_LOW + 1;
int dir1 = 1;
int dir2 = 1;

Servo myservo1;  // create servo object to control a servo
Servo myservo2;

void setup() {
    Serial.begin(115200);

    // Set up ultrasonic sensor 
    pinMode(ULTRA_TRG, OUTPUT); 
    pinMode(ULTRA_ECHO, INPUT); 

    // Set up servos 
    myservo1.attach(SERVO_PIN1); 
    // myservo2.attach(SERVO_PIN2);
}

// get a reading from the ultrasonic sensor, return distance in cm. 
float ping() {
  digitalWrite(ULTRA_TRG, LOW);
  delayMicroseconds(2);
  digitalWrite(ULTRA_TRG, HIGH);
  delayMicroseconds(10);
  digitalWrite(ULTRA_ECHO, LOW);
  float distance = pulseIn(ULTRA_ECHO, HIGH, 50000) / 58.2;
  return distance;
}

void loop() {
  
    if (pos1 <= ONE_LOW || pos1 >= ONE_HIGH) {
        dir1 *= -1;
    }
    pos1 += dir1;
    myservo1.write(pos1);

    distance = (int) ping(); 
    distance = (distance != 0) ? distance : 400;

    Serial.println(String(distance) + "   " + String(pos1) + "   " + String(pos2));
    delay(10);
}
