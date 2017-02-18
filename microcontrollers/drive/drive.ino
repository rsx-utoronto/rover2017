/*
  Drive Arduino Program
    RSX: connect using Node server or any TCP connection. Use port numbers specifed below to connect.
    Supports two connections, one for Base Station Node server, other for autnomous software
 Circuit:
 * Ethernet shield attached to pins 10, 11, 12, 13
 */

#include <SPI.h>
#include <Ethernet.h>
#include <Servo.h>

// Enter a MAC address and IP address for your controller below.
// The IP address will be dependent on your local network.
// gateway and subnet are optional:
byte mac[] = {
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED
};
IPAddress ip(192, 168, 0, 177);
IPAddress myDns(192,168,1, 1);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);

#define baseStationPort 5000
#define autoSysPort 6000

EthernetServer baseConn(baseStationPort);
EthernetServer autoSysConn(autoSysPort);

//SyRen
//Left Motor back
int pin_speed1  = 2;
int dir1  = 3;

//Left Motor middle
int pin_speed2  = 26;
int dir2  = 5;

//Left Motor front
int pin_speed3  = 6;
int dir3  = 7;

//Right Motor back
int pin_speed4  = 8;
int dir4  = 9;

//Right Motor middle
int pin_speed5 = 28;
int dir5 = 11;

//Right Motor forward
int pin_speed6 = 12;
int dir6 = 13;

void setup() {
  //Set pins as outputs
  pinMode(pin_speed1, OUTPUT);
  pinMode(pin_speed2, OUTPUT);
  pinMode(pin_speed3, OUTPUT);
  pinMode(pin_speed4, OUTPUT);
  pinMode(pin_speed5, OUTPUT);
  pinMode(pin_speed6, OUTPUT);
  pinMode(dir1, OUTPUT);
  pinMode(dir2, OUTPUT);
  pinMode(dir3, OUTPUT);
  pinMode(dir4, OUTPUT);
  pinMode(dir5, OUTPUT);
  pinMode(dir6, OUTPUT);
  
  // initialize the ethernet device
  Ethernet.begin(mac, ip, myDns, gateway, subnet);
  // start listening for clients
  baseConn.begin();
  autoSysConn.begin();
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  Serial.print("IP address:");
  Serial.println(Ethernet.localIP());
}

//Stop the motor
void stop(){
    analogWrite(pin_speed1, 0);
    analogWrite(pin_speed2, 0);
    analogWrite(pin_speed3, 0);
    analogWrite(pin_speed4, 0);
    analogWrite(pin_speed5, 0);
    analogWrite(pin_speed6, 0);
}

//Pivot left
void pivotL(int pivot){
    //Stop the motors first
    stop();

    //Set all the left motor dirs to backwards
    digitalWrite(dir1, LOW);
    digitalWrite(dir2, LOW);
    digitalWrite(dir3, LOW);

    //Set all the right motor dirs to forwards
    digitalWrite(dir4, HIGH);
    digitalWrite(dir5, HIGH);
    digitalWrite(dir6, HIGH);

    //Set all the speed to the pivoting speed
    //Left motors
    analogWrite(pin_speed1, pivot);
    analogWrite(pin_speed2, pivot);
    analogWrite(pin_speed3, pivot);
    //Right motors
    analogWrite(pin_speed4, pivot);
    analogWrite(pin_speed5, pivot);
    analogWrite(pin_speed6, pivot);
}
//Pivot right
void pivotR(int pivot){
    //Stop the motors first
    stop();

    //Set all the left motor dirs to forwards
    digitalWrite(dir1, HIGH);
    digitalWrite(dir2, HIGH);
    digitalWrite(dir3, HIGH);

    //Set all the right motor dirs to backwards
    digitalWrite(dir4, LOW);
    digitalWrite(dir5, LOW);
    digitalWrite(dir6, LOW);

    //Set all the speed to the pivoting speed
    //Left motors
    analogWrite(pin_speed1, pivot);
    analogWrite(pin_speed2, pivot);
    analogWrite(pin_speed3, pivot);
    //Right motors
    analogWrite(pin_speed4, pivot);
    analogWrite(pin_speed5, pivot);
    analogWrite(pin_speed6, pivot);
}

void forward(int speedl, int speedr){
    //Stop the motors first
    stop();

    //Set all the dir to forward
    digitalWrite(dir1, HIGH);
    digitalWrite(dir2, HIGH);
    digitalWrite(dir3, HIGH);
    digitalWrite(dir4, HIGH);
    digitalWrite(dir5, HIGH);
    digitalWrite(dir6, HIGH);

    //Set all the speed
    //Left motors
    analogWrite(pin_speed1, speedl);
    analogWrite(pin_speed2, speedl);
    analogWrite(pin_speed3, speedl);
    //Right motors
    analogWrite(pin_speed4, speedr);
    analogWrite(pin_speed5, speedr);
    analogWrite(pin_speed6, speedr);
    
}
void backward(int speedl, int speedr){
    //Stop the motors first
    stop();

    //Set all the dir to backwards
    digitalWrite(dir1, LOW);
    digitalWrite(dir2, LOW);
    digitalWrite(dir3, LOW);
    digitalWrite(dir4, LOW);
    digitalWrite(dir5, LOW);
    digitalWrite(dir6, LOW);

    //Set all the speed
    //Left motors
    analogWrite(pin_speed1, speedl);
    analogWrite(pin_speed2, speedl);
    analogWrite(pin_speed3, speedl);
    //Right motors
    analogWrite(pin_speed4, speedr);
    analogWrite(pin_speed5, speedr);
    analogWrite(pin_speed6, speedr);
}


// Ethernet helper function
void processData(EthernetClient * client, EthernetServer * server){
  String buff = "";
  while (client->available() > 0) {
      // read the bytes incoming from the client:
      char thisChar = client->read();
      buff += thisChar;
  }

  if(buff.length() != 15) {
    Serial.print("bad buffer: ");
  }

  Serial.println(buff);

  int speedl = buff.substring(0, 5).toInt();
  int speedr = buff.substring(5, 10).toInt();
  int pivot = buff.substring(10, 14).toInt();
  boolean driveMode = buff.charAt(14) == '1';
  Serial.print(speedl); 
  Serial.print(speedr); 
  Serial.println(pivot); 
  
  
  if(driveMode && speedl > 0) {
    forward(speedl, speedr);
  }
  else if (driveMode && speedl < 0) {
    backward(-speedl, -speedr);
  }
  else if (pivot < 0) {
    pivotL(-pivot);
  }
  else if (pivot > 0) {
    pivotR(pivot);
  }
  else {
    stop();
  }
}

void loop() {
  // wait for a new client:
  EthernetClient baseClient = baseConn.available();
  EthernetClient autoSysClient = autoSysConn.available();

  if(autoSysClient){
     processData(&autoSysClient, &autoSysConn);
  }

  else if(baseClient) {
    processData(&baseClient, &baseConn);
  }
}


/*
  Read sensors and print to console
  Format: ```
  Temperatures 1 2 3 4 5 6
  Currents 1 2 3 4 5 6
  ```
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
*/
