/* 
  Drive Arduino Program
    RSX: connect using Node server or any TCP connection. Use port numbers specifed below to connect.
    Supports two connections, one for Base Station Node server, other for autnomous software
 Circuit:
 * Ethernet shield attached to pins 10, 11, 12, 13
 */

#define MINI_ROVER    0  // whether we're using the mini rover

//L293D
//Joint Motor 1
int speedPins[] = {5, 8, 13, 6, 5, 7 } ;
int directionPins[] = {9, 28, 12, 10, 26, 6 };

int speedPinsUno[] = {5, 6} ;
int directionPinsUno[] = {9, 10};

int speedl;
int speedr;
boolean driveMode;
int pivot;
int speedf = -255;
int speedp = -255;

void setup() {
  //Set pins as outputs
  for (int i=0; i<6; i++) {
    pinMode(speedPins[i], OUTPUT);
    pinMode(directionPins[i], OUTPUT);
  }

  // Open serial communications and wait for port to open:
  Serial.begin(38400);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
}

// Helper functions
#if MINI_ROVER
#pragma message ("using mini rover") 
void setLeftSpd(int spd) {
      if (spd > 0){
        analogWrite(speedPins[0], spd);
        analogWrite(speedPins[1], 0);
      }
      else{
        analogWrite(speedPins[0], 0);
        analogWrite(speedPins[1], -spd);
      }
}

void setRightSpd(int spd) {
      if (spd > 0){
        analogWrite(speedPins[2], spd);
        analogWrite(speedPins[3], 0);
      }
      else{
        analogWrite(speedPins[2], 0);
        analogWrite(speedPins[3], -spd);
      }
}
#else // not mini rover
#pragma message ("using big rover")
void setLeftSpd(int spd) {
        Serial.print("left speed ");
      Serial.println(spd);
      if(spd < 0) {
          //for(int i=0; i<3; i++) {
              //digitalWrite(directionPins[i], LOW);
              //analogWrite(speedPins[i], -spd);
          //}
          digitalWrite(directionPinsUno[0], LOW);
          analogWrite(speedPinsUno[0], -spd);
      }
      else {
          //for(int i=0; i<3; i++) {
              //digitalWrite(directionPins[i], HIGH);
              //analogWrite(speedPins[i], spd);
          //}
          digitalWrite(directionPinsUno[0], HIGH);
          analogWrite(speedPinsUno[0], spd);
      }
}

void setRightSpd(int spd) {
      Serial.print("right speed ");
      Serial.println(spd);
    if(spd < 0) {
        //for(int i=3; i<6; i++) {
            //digitalWrite(directionPins[i], LOW);
            //analogWrite(speedPins[i], -spd);
        //}
        digitalWrite(directionPinsUno[1], LOW);
        analogWrite(speedPinsUno[1], -spd);
    }
    else {
        //for(int i=3; i<6; i++) {
            //digitalWrite(directionPins[i], HIGH);
            //analogWrite(speedPins[i], spd);
        //}
        digitalWrite(directionPinsUno[1], HIGH);
        analogWrite(speedPinsUno[1], spd);
    }
}
#endif // mini rover

// Stop the motor
void stop(){
    setLeftSpd(0);
    setRightSpd(0);
}

// Pivot either direction
void doPivot(int pivot){
    setLeftSpd(pivot);
    setRightSpd(-pivot);
}

// Drive forward or backward
void forward(int speedl, int speedr){
    setLeftSpd(speedl);
    setRightSpd(speedr);
}

/* Load `len` values from serial into result. Add a null character at the end */
void loadData(char* result, unsigned len) {
  if(Serial.available() < len) {
    result = "\0";
  }

  for(int i=0; i<len; i++) {
    result[i] = Serial.read();
  }
  result[len] = 0; // null terminate the string so atoi works
}

// Ethernet helper function
void processData() {
  if(Serial.available() < 16) {
    return;
  }
  Serial.println("started a write");
  Serial.println(millis());

  char lSpeedBuffer[6], rSpeedBuffer[6], pivotBuffer[6], driveMode;
  loadData(lSpeedBuffer, 5);
  loadData(rSpeedBuffer, 5);
  loadData(pivotBuffer, 5);
  driveMode = Serial.read();

  int speedl = atoi(lSpeedBuffer);
  int speedr = atoi(rSpeedBuffer);
  int pivot = atoi(pivotBuffer);

  if(driveMode == '1') {
    forward(-speedl, -speedr);
  }
  else {
    doPivot(pivot);
  }

  // clear serial port  
  while(Serial.available()) {
    Serial.read();
  }
  
  Serial.println("done writing"); 
  Serial.println(millis());
}

void loop() {
  // wait for a new client:
  delay(5);
  processData();
}

