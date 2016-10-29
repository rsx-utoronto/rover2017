// Drive System Code

// sensors: photo cell
const int photocellPin = 0;

//motor1
const int InA1 = 2; // forward
const int InB1 = 3; // backward

//motor2
const int InA2 = 4;
const int InB2 = 5;
const int Forwardpin = 8;
const int PivotRpin = 9;
const int PivotLpin = 10;

void setup() {
  Serial.begin(9600);
  pinMode(InA1, OUTPUT);
  pinMode(InB1, OUTPUT);

  pinMode(InA2, OUTPUT);
  pinMode(InB2, OUTPUT);

  pinMode(Forwardpin, OUTPUT);
  pinMode(PivotRpin, OUTPUT);
  pinMode(PivotLpin, OUTPUT);
  
}

void loop() {
  readSensors();  
  delay(10); // give the server time to process
  parseDrive(); 
  delay(200); 
}

/*
  Read the drive control from the Serial port
*/
void parseDrive() {
  int speedl = Serial.parseInt();
  int speedr = Serial.parseInt();
  int pivot = Serial.parseInt();
  int driveMode = Serial.parseInt();

  while(Serial.available()){ 
    char x = Serial.read(); 
    if (x == '\n') break; 
  }

  if (driveMode != 0) {
    forward();
    digitalWrite(Forwardpin, HIGH);
    digitalWrite(PivotRpin, LOW);
    digitalWrite(PivotLpin, LOW);
  }
  else if (pivot > 0) {
    pivotR();
    digitalWrite(PivotRpin, HIGH);
    digitalWrite(Forwardpin, LOW);
    digitalWrite(PivotLpin, LOW);
  }
  else {
    pivotL();
    digitalWrite(PivotLpin, HIGH);
    digitalWrite(PivotRpin, LOW);
    digitalWrite(Forwardpin, LOW);
  }
}

void forward() {
  digitalWrite(InA1, HIGH);
  digitalWrite(InB1, LOW);

  digitalWrite(InA2, HIGH);
  digitalWrite(InB2, LOW);
}

void pivotR() {
  digitalWrite(InA1, HIGH);
  digitalWrite(InB1, LOW);

  digitalWrite(InA2, LOW);
  digitalWrite(InB2, HIGH);
}

void pivotL() {
  digitalWrite(InA1, LOW);
  digitalWrite(InB1, HIGH);

  digitalWrite(InA2, HIGH);
  digitalWrite(InB2, LOW);
}

/*
  Read sensors and print to console
  Format: ```
  Temperatures 1 2 3 4 5 6
  Currents 1 2 3 4 5 6
  ```
 */
void readSensors() {
  float Vout = analogRead(photocellPin);
  float Temp = (Vout / 1024.0) * 5000; //convert to millivolts
  float cel = Temp / 10; //get temperature in celcius (1Cel/10mv ratio)

  String toPrint = "temperatures "; 
  for (int i = 0; i<6; i++){
    toPrint += String(cel + i) + " ";  // change me when we get actual sensors! 
  }
  Serial.println(toPrint); 

  toPrint = "currents "; 
  for (int j = 0; j<6; j++){
    toPrint += String(10.0 + j) + " ";  // change me when we get actual sensors! 
  }
  Serial.println(toPrint);
}
