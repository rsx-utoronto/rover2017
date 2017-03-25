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
int speedPins[] = {3, 5, 6, 9}; 
//int directionPins[] = {2, 26, 6, 8, 28, 12}; 

int speedl;
int speedr;
boolean driveMode;
int pivot; 
int speedf = -255;
int speedp = -255;
const int max_speed = 128;
const int min_speed = 50;
const int joyDead = 8; //Range of joystick movement that is accidental
const int joy_max = 255;
float drive_exp = 1.4;  // Exponential speed (1= linear, 2= squared)

void setup() {
  //Set pins as outputs
  for (int i=0; i<6; i++) {
    pinMode(speedPins[i], OUTPUT); 
    //pinMode(directionPins[i], OUTPUT); 
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

int sgn(int x){
    if (x > 0) return 1;
    if (x < 0) return -1;
    return 0;
}

// Drive forward or backward 
void forward(int speedl, int speedr){
    setLeftSpd(speedl); 
    setRightSpd(speedr); 
}

float expDrive (int joyVal){
    int joyMax = joy_max - joyDead;
    int joySign = sgn(joyVal);
    int joyLive = abs(joyVal) - joyDead;
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
  
  Serial.println("Speed values");
  Serial.println(speedl); 
  float exp_speedl = expDrive(speedl);
  Serial.println(exp_speedl); 
  Serial.println(speedr); 
  float exp_speedr = expDrive(speedr);
  Serial.println(exp_speedr); 
  Serial.println("Pivot value");
  Serial.println(pivot); 
  float exp_pivot = expDrive(pivot);
  Serial.println(exp_pivot);

  if(driveMode) {
    Serial.println("going forward"); 
    forward(exp_speedl, exp_speedr);
  }
  else if (!driveMode) {
    Serial.println("Pivoting left"); 
    doPivot(-exp_pivot);
  }
}

void loop() {
  
  if (speedf<255){
    int speedl = speedf;
    int speedr = speedf;
    boolean driveMode = true;
    speedf++;
  }
  if (speedf>255){
    delay(3000);
    boolean driveMode = false;
    int pivot = speedp;
    speedp++;
  }

  if (speedp > 255){
    stop();
  }

  Serial.println("Speed values");
  Serial.println(speedl); 
  float exp_speedl = expDrive(speedl);
  Serial.println(exp_speedl); 
  Serial.println(speedr); 
  float exp_speedr = expDrive(speedr);
  Serial.println(exp_speedr); 
  Serial.println("Pivot value");
  Serial.println(pivot); 
  float exp_pivot = expDrive(pivot);
  Serial.println(exp_pivot);
  
  if(driveMode) {
    Serial.println("going forward"); 
    forward(exp_speedl, exp_speedr);
  }
  else if (!driveMode) {
    Serial.println("Pivoting left"); 
    doPivot(-exp_pivot);
  }

}

