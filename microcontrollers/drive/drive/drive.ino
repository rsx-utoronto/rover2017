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
int speedPins[] = {3, 5, 7, 9, 11, 13} ; 
int directionPins[] = {2, 26, 6, 8, 28, 12}; 

const int max_speed = 128;
const int min_speed = 50;
const int joydead = 8; //Range of joystick movement that is accidental
const int joy_max = 255;
float drive_exp = 1.4;  // Exponential speed (1= linear, 2= squared)

void setup() {
  //Set pins as outputs
  for (int i=0; i<6; i++) {
    pinMode(speedPins[i], OUTPUT); 
    pinMode(directionPins[i], OUTPUT); 
  }
    
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

// Helper functions
void setLeftSpd(int spd) { 
      if(spd < 0) {
          for(int i=0; i<3; i++) {
              digitalWrite(directionPins[i], LOW); 
              analogWrite(speedPins[i], -spd); 
          }
      }
      else { 
          for(int i=0; i<3; i++) {
              digitalWrite(directionPins[i], HIGH); 
              analogWrite(speedPins[i], spd);  
          }    
      }
}

void setRightSpd(int spd) { 
    if(spd < 0) { 
        for(int i=3; i<6; i++) {
            digitalWrite(directionPins[i], LOW); 
            analogWrite(speedPins[i], -spd); 
        }
        digitalWrite(directionPins[4], HIGH);
        digitalWrite(directionPins[5], HIGH); 
    }
    else { 
        for(int i=3; i<6; i++) {
            digitalWrite(directionPins[i], HIGH); 
            analogWrite(speedPins[i], spd);  
        }    
        digitalWrite(directionPins[4], LOW); 
        digitalWrite(directionPins[5], LOW); 
    }
}

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

int sgn(int x){
    if (x > 0) return 1;
    if (x < 0) return -1;
    return 0;
}

float expDrive (int joyVal){
    int joyMax = joy_max - joydead;
    int joySign = sign(joyVal);
    int joyLive = abs(joyVal) - joydead;
    return joySign * (min_speed + ((max_speed - min_speed) * pow(joyLive, drive_exp) / pow(joyMax, drive_exp)));
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
  
  exp_speedl = expDrive(speedl); 
  exp_speedr = expDrive(speedr);
  exp_pivot = expDrive(pivot);

  if(speedl == 0){
    exp_speedl = 0;
  }
  if(speedr == 0){
    exp_speedr = 0;
  }
  if(pivot == 0){
    exp_pivot = 0;
  }

  if(driveMode) {
    forward(exp_speedl, exp_speedr);
  }
  else if (!driveMode) {
    doPivot(-exp_pivot);
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
  delay(10); 
}
