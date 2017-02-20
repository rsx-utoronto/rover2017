#include <Servo.h>

unsigned long pulse_width;

const int SERVO_PIN1 = 7;    // left and right
const int SERVO_PIN2 = 8;    // up and down
const int ONE_LOW = 80;      // 124 is middle
const int ONE_HIGH = 168;
const int TWO_LOW = 40;      // not used for demo
const int TWO_HIGH = 120;

int pos1 = ONE_LOW + 1;
int pos2 = TWO_LOW + 1;
int dir1 = 1;
int dir2 = 1;

Servo myservo1;  // create servo object to control a servo
Servo myservo2;

void setup() {
    Serial.begin(115200);
    pinMode(2, OUTPUT); // Set pin 2 as trigger pin
    pinMode(3, INPUT); // Set pin 3 as monitor pin
    digitalWrite(2, LOW); // Set trigger LOW for continuous read
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
    pos2 = 90;
    myservo1.write(pos1);
    myservo2.write(pos2);

    pulse_width = pulseIn(3, HIGH); // Count how long the pulse is high in microseconds
    if(pulse_width != 0){ // If we get a reading that isn't zero, let's print it
        pulse_width = pulse_width/10; // 10usec = 1 cm of distance for LIDAR-Lite
    } else {
        pulse_width = 0;
    }

    Serial.println(String(pulse_width) + "   " + String(pos1) + "   " + String(pos2));
//    delay(10);
}