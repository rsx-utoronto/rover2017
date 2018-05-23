/*
  Drive Arduino Program
    RSX: connect using Node server or any TCP connection. Use port numbers specifed below to connect.
    Supports two connections, one for Base Station Node server, other for autnomous software
 Circuit:
 * Ethernet shield attached to pins 10, 11, 12, 13
 */

#define MINI_ROVER    0  // whether we're using the mini rover

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
int speedPins[] = {9, 11, 13, 3, 5, 7 } ;
int directionPins[] = {8, 28, 12, 2, 26, 6 };

int speedl;
int speedr;
boolean driveMode;
int pivot;
int speedf = -255;
int speedp = -255;
/*
const int max_speed = 128;
const int min_speed = 50;
const int joyDead = 0; //Range of joystick movement that is accidental
const int joy_max = 100;
float drive_exp = 1.6;  // Exponential speed (1= linear, 2= squared)
*/
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
    }
    else {
        for(int i=3; i<6; i++) {
            digitalWrite(directionPins[i], HIGH);
            analogWrite(speedPins[i], spd);
        }
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
/*
int sgn(int x){
    if (x > 0) return 1;
    if (x < 0) return -1;
    return 0;
}
*/

// Drive forward or backward
void forward(int speedl, int speedr){
    setLeftSpd(speedl);
    setRightSpd(speedr);
}
/*
float expDrive (int joyVal){
    int joyMax = joy_max - joyDead;
    int joySign = sgn(joyVal);
    int joyLive = abs(joyVal) - joyDead;
    return joySign * (min_speed + ((max_speed - min_speed) * pow(joyLive, drive_exp) / pow(joyMax, drive_exp)));
}
*/
// Ethernet helper function
void processData(EthernetClient * client, EthernetServer * server){
  String buff = "";
  while (client->available() > 0) {
      // read the bytes incoming from the client:
      char thisChar = client->read();
      
      buff += thisChar;
  }

  if(buff.length() % 15 != 0) {
    Serial.print("bad buffer: ");
    Serial.print(buff.length());
  }
  Serial.println(buff);

  int frameshift = buff.length() - 15; // if we have more than one buffer, take the last one

  int speedl = buff.substring(0 + frameshift, 5 + frameshift).toInt();
  int speedr = buff.substring(5 + frameshift, 10 + frameshift).toInt();
  int pivot = buff.substring(10 + frameshift, 14 + frameshift).toInt();
  boolean driveMode = (buff.charAt(14 + frameshift) == '1');

  if(driveMode) {
    forward(-speedl, -speedr);
  }
  else {
    doPivot(pivot);
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
  delay(5);

}
