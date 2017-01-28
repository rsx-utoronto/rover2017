/*
  Drive Arduino Program
    RSX: connect using Node server or any TCP connection. Use port numbers specifed below to connect.
    Supports two connections, one for Base Station Node server, other for autnomous software

 Circuit:
 * Ethernet shield attached to pins 10, 11, 12, 13

 */

#include <SPI.h>
#include <Ethernet.h>

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


// sensors: photo cell
const int photocellPin = 0;

// drive system: motor1
const int InA1 = 2; // forward
const int InB1 = 3; // backward

// drive system: motor2
const int InA2 = 4;
const int InB2 = 5;

// drive system: PWM input
const int enA = 6;
const int enB = 9;


void setup() {
  pinMode(InA1, OUTPUT);
  pinMode(InB1, OUTPUT);

  pinMode(InA2, OUTPUT);
  pinMode(InB2, OUTPUT);

  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);

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

// Drive helper functions
void forward(int speedl, int speedr) {
  digitalWrite(InA1, HIGH);
  digitalWrite(InB1, LOW);
  analogWrite(enA, speedl);

  digitalWrite(InA2, HIGH);
  digitalWrite(InB2, LOW);
  analogWrite(enB, speedr);
}
void pivotR(int speedl, int speedr) {
  digitalWrite(InA1, HIGH);
  digitalWrite(InB1, LOW);
  analogWrite(enA, speedl);

  digitalWrite(InA2, LOW);
  digitalWrite(InB2, HIGH);
  analogWrite(enB, speedr);
}
void stop() {
  digitalWrite(InA1, LOW);
  digitalWrite(InB1, LOW);
  digitalWrite(InA2, LOW);
  digitalWrite(InB2, LOW);
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
    Serial.print("bad buffer");
    Serial.print(buff);
  }

  int speedl = buff.substring(0, 5).toInt();
  int speedr = buff.substring(5, 10).toInt();
  int pivot = buff.substring(10, 14).toInt();
  boolean driveMode = buff.charAt(14) == '1';

  if(driveMode) {
    forward(speedl, speedr);
  }
  else if (pivot > 0) {
    pivotR(speedl, speedr);
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
