#include <SPI.h>
#include <Ethernet.h>

byte mac[] = {
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xEE
};
IPAddress ip(192, 168, 0, 180);
IPAddress myDns(192,168,1, 1);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 0, 0);

#define baseStationPort 5000
#define autoSysPort 6000

EthernetServer baseConn(baseStationPort);
EthernetServer autoSysConn(autoSysPort);

const int CURRENT_PINS[] = {A0, A1, A2, A3, A4, A5}; 
const int RELAY_PINS[] = {2, 3, 5, 6, 7, 8}; // 4 is reserved for ethernet shields

float lastCurrents[] = {0,0,0,0,0,0}; 
boolean relayOn[] = {false, false, false, false, false, false}; 

void setup() {
  for(int i=0; i<6; i++) {
    pinMode(CURRENT_PINS[i], INPUT); 
    pinMode(RELAY_PINS[i], OUTPUT); 
  }
  
  // initialize the ethernet device
  Ethernet.begin(mac, ip, myDns, gateway, subnet);
  // start listening for clients
  baseConn.begin();
  autoSysConn.begin();
  
  Serial.begin(9600);
  Serial.print("IP address:");
  Serial.println(Ethernet.localIP());
}

// Returns current in amps 
float readCurrent(int index) { 
  return (4.88/13.3)*(analogRead(CURRENT_PINS[index])-512);
}

// Sets the state of a relay
void setRelay(int index, boolean value) {
  relayOn[index] = value; 
}

void processData(EthernetClient * client) { 
  String buff = ""; 
  while(client->available() > 0) { 
    char thisChar = client->read(); 
    buff += thisChar; 
  }

  if(buff.length() != 6) {
    Serial.print("Bad buffer: "); 
  }
  Serial.print(buff); 

  for(int i=0; i<6; i++) {
    setRelay(i, buff.charAt(i) == '1'); 
    client->print(lastCurrents[i]); 
    client->print(","); 
  }
}

void loop() {
  for(int i=0; i<6; i++) {
    lastCurrents[i] = readCurrent(i); 
    setRelay(i, relayOn[i]); 
  }
  delay(10); 
}
