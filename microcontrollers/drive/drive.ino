/*
  Drive Arduino Program
 */

int speedPins[] = {10, 3, 5, 11, 9, 6};
int directionPins[] = {4, 4, 4, 2, 2, 2};

int speedl;
int speedr;
boolean driveMode;
int pivot;
int speedf = -255;
int speedp = -255;

void setup() {
  //Set pins as outputs
  for (int i = 0; i < 6; i++) {
    pinMode(speedPins[i], OUTPUT);
    pinMode(directionPins[i], OUTPUT);
    analogWrite(speedPins[i], 0);
    digitalWrite(directionPins[i], LOW);
  }

  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connectx. Needed for native USB port only
  }
}

// Helper functions
/* Takes a speed from -255 to 255, maps it to 255 to 0 */
void setLeftSpd(int spd) {
  for (int i = 0; i < 3; i++) {
    analogWrite(speedPins[i], abs(spd));
    digitalWrite(directionPins[i], spd > 0 ? HIGH : LOW);
  }
}

void setRightSpd(int spd) {
    for (int i = 3; i < 6; i++) {
      analogWrite(speedPins[i], abs(spd));
      digitalWrite(directionPins[i], spd > 0 ? HIGH : LOW);
    }
}

// Stop the motor
void stop() {
  setLeftSpd(0);
  setRightSpd(0);
}

// Pivot either direction
void doPivot(int pivot) {
  setLeftSpd(pivot);
  setRightSpd(-pivot);
}

// Drive forward or backward
void forward(int speedl, int speedr) {
  setLeftSpd(speedl);
  setRightSpd(speedr);
}

/* Load `len` values from serial into result. Add a null character at the end */
void loadData(char* result, unsigned len) {
  if (Serial.available() < len) {
    result = "\0";
  }

  for (int i = 0; i < len; i++) {
    result[i] = Serial.read();
  }
  result[len] = 0; // null terminate the string so atoi works
}

// Ethernet helper function
void processData() {
  if (Serial.available() < 16) {
    return;
  }

  char lSpeedBuffer[6], rSpeedBuffer[6], pivotBuffer[6], driveMode;
  loadData(lSpeedBuffer, 5);
  loadData(rSpeedBuffer, 5);
  loadData(pivotBuffer, 5);
  driveMode = Serial.read();

  int speedl = atoi(lSpeedBuffer);
  int speedr = atoi(rSpeedBuffer);
  int pivot = atoi(pivotBuffer);
//  Serial.println(lSpeedBuffer);///
//  Serial.println(rSpeedBuffer);/
//  Serial.println(pivotBuffer);/

  if (driveMode == '1') {
    forward(-speedl, -speedr);
  }
  else {
    doPivot(pivot);
  }

  // clear serial port
  while (Serial.available()) {
    Serial.read();
  }
}

void loop() {
  // wait for a new client:
  delay(5);
  processData();
}

