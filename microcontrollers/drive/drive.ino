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

//L293D
//Joint Motor 1
int inA1  = 2;
int inB1  = 3;

//Joint Motor 2
int inA2  = 4;
int inB2  = 5;

//Middle Motor 3
int inA3  = 6;
int inB3  = 7;

//Middle Motor 4
int inA4  = 8;
int inB4  = 9;

//Motor speed
int mSpeed = 150;


void setup() {
  //Set pins as outputs
  pinMode(inA1, OUTPUT);
  pinMode(inA2, OUTPUT);
  pinMode(inA3, OUTPUT);
  pinMode(inA4, OUTPUT);
  pinMode(inB1, OUTPUT);
  pinMode(inB2, OUTPUT);
  pinMode(inB3, OUTPUT);
  pinMode(inB4, OUTPUT);

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
    analogWrite(inB1, 0);
    analogWrite(inA1, 0);
    analogWrite(inB2, 0);
    analogWrite(inA2, 0);

    //Middle motors
    analogWrite(inB3, 0);
    analogWrite(inA3, 0);
    analogWrite(inB4, 0);
    analogWrite(inA4, 0);
}

//Pivot left
void pivotL(int pivot){
    analogWrite(inB1, pivot);
    analogWrite(inA1, 0);
    analogWrite(inB2, 0);
    analogWrite(inA2, pivot);

    //Middle motors
    analogWrite(inB3, 0);
    analogWrite(inA3, 0);
    analogWrite(inB4, 0);
    analogWrite(inA4, 0);
}
//Pivot right
void pivotR(int pivot){
    analogWrite(inB1, 0);
    analogWrite(inA1, pivot);
    analogWrite(inB2, pivot);
    analogWrite(inA2, 0);

    //Middle motors
    analogWrite(inB3, 0);
    analogWrite(inA3, 0);
    analogWrite(inB4, 0);
    analogWrite(inA4, 0);
}

void forward(int speedl, int speedr){
    analogWrite(inB1, speedl);
    analogWrite(inA1, 0);
    analogWrite(inB2, speedl);
    analogWrite(inA2, 0);

    //Middle motors
    analogWrite(inB3, speedl);
    analogWrite(inA3, 0);
    analogWrite(inB4, 0);
    analogWrite(inA4, speedl);
}
void backward(int speedl, int speedr){
    analogWrite(inA1, speedl);
    analogWrite(inB1, 0);

    analogWrite(inA2, speedl);
    analogWrite(inB2, 0);

    //Middle motors
    analogWrite(inB3, 0);
    analogWrite(inA3, speedl);

    analogWrite(inB4, speedl);
    analogWrite(inA4, 0);
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

  if(driveMode && speedl > 0) {
    forward(speedl, speedr);
  }
  else if (driveMode && speedl < 0) {
    backward(-speedl, -speedr);
  }
  else if (pivot < 0) {
    pivotL(pivot);
  }
  else if (pivot > 0) {
    pivotR(-pivot);
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