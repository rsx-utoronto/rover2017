/*
  Drive Arduino Program
 */

int speedPins[] = {10, 3, 5, 11, 9, 6};
int directionPins[] = {4, 4, 4, 2, 2, 2};

unsigned long last_update = 0;

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
  while (!Serial); // wait for serial port to connectx. Needed for native USB port only
  Serial.setTimeout(2); // 2ms timeout
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

void process_data() {
  if (!Serial.available()) return;
  switch (Serial.read()) {
    case 'n': // normal operation
      Serial.read();
      setLeftSpd(Serial.parseInt());
      setRightSpd(Serial.parseInt());
      last_update = millis();
      break;
    default:
      Serial.println("parse err");
  }
}

void loop() {
  process_data();
  if (millis() - last_update > 2000){
    stop();
  }
}

