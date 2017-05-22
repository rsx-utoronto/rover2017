#include <SPI.h>
#include <Ethernet.h>
#include <Servo.h>

#define NUM_SENSORS   9

byte mac[] = {
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xEE
};
IPAddress ip(192, 168, 0, 179);
IPAddress myDns(192, 168, 1, 1);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 0, 0);

#define baseStationPort 5000
#define autoSysPort 6000

EthernetServer baseConn(baseStationPort);
EthernetServer autoSysConn(autoSysPort);

const int SENSOR_PINS[NUM_SENSORS] = {A0, A1, A2, A3, A4, A5, A6, A7, A8};
const int CAROUSEL_PIN = 6; // science carousel: four settings
const int DRILL_PIN = 7; // opening and closing drill

int sensorReadings[NUM_SENSORS]; // raw sensor reaidngs

Servo carousel, drill;
int carouselAngles[] = {2, 60, 120, 178};
int carouselAngle = carouselAngles[0];
int drillAngles[] = {10, 40};
int drillAngle = drillAngles[0];

void setup() {
  for(int i=0; i<6; i++) {
    pinMode(SENSOR_PINS[i], INPUT);
  }

  carousel.attach(CAROUSEL_PIN);
  drill.attach(DRILL_PIN);

  // initialize the ethernet device
  Ethernet.begin(mac, ip, myDns, gateway, subnet);
  // start listening for clients
  baseConn.begin();
  autoSysConn.begin();

  Serial.begin(9600);
  Serial.print("IP address:");
  Serial.println(Ethernet.localIP());
}

int ctoi(char c) { 
  return c - 48; 
}

// Reads two integers {carousel_state}{drill state} that matches /[0-3][0-1]/
// The states are looked up in the Angles tables.
// Writes the raw sensor values as comma separated values.
void processData(EthernetClient * client) {
  String buff = "";
  while(client->available() > 0) {
    char thisChar = client->read();
    buff += thisChar;
  }

  // write data from the sensors
  for(int i=0; i<NUM_SENSORS; i++) {
    client->print(sensorReadings[i]);
    client->print(",");
  }
  client->print("\n");

  if(buff.length() % 2 != 0) {
    Serial.print("Bad buffer: ");
    Serial.println(buff);
    return;
  }

  carouselAngle = carouselAngles[ctoi(buff.charAt(0))];
  drillAngle = drillAngles[ctoi(buff.charAt(1))];
}

void loop() {
  for (int i=0; i<NUM_SENSORS; i++) {
    sensorReadings[i] = analogRead(SENSOR_PINS[i]);
  }

  carousel.write(carouselAngle);
  drill.write(drillAngle);
  delay(10);
}
