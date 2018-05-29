#include <Wire.h>
#define SLAVE_ADDRESS 4


int pwmPin1 = 2;
int dir1 = 34;

void setup() {
  // put your setup code here, to run once:
  Wire.begin();
  Serial.begin(9600);


  pinMode(pwmPin1, OUTPUT);
  pinMode(dir1, OUTPUT);


}

void loop() {
  digitalWrite(dir1,HIGH);
  analogWrite(pwmPin1, 80);

  Wire.requestFrom(SLAVE_ADDRESS,1);
  while (Wire.available()){
    byte encoderCount = Wire.read();
    Serial.println(encoderCount,DEC);
  }
  delay(200);
}
