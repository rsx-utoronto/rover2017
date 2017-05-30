#include <SPI.h>
#include <Ethernet.h>

byte mac[] = {
  0xDE, 0xAD, 0xBE, 0xEF, 0xFF, 0xEE
};
IPAddress ip(192, 168, 0, 180);
IPAddress myDns(192,168,1, 1);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 0, 0);

#define baseStationPort 5000
#define autoSysPort 6000

EthernetServer baseConn(baseStationPort);
EthernetServer autoSysConn(autoSysPort);

const int CURRENT_PINS[] = {A10, A11, A12, A13, A14, A15}; 
const int RELAY_PINS[] = {2, 3, 8, 7, 5, 6}; // 4 is reserved for ethernet shields

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
  Serial.println(analogRead(CURRENT_PINS[index]));
  return (25./256.)*(analogRead(CURRENT_PINS[index])-523);
}

// Sets the state of a relay
void setRelay(int index, boolean value) {
  relayOn[index] = value; 
  digitalWrite(RELAY_PINS[index], value ? LOW : HIGH);  // LOW means relay is conducting
}

void processData(EthernetClient * client, EthernetServer * server) { 
  Serial.println("processing data"); 
  String buff = ""; 
  while(client->available() > 0) { 
    char thisChar = client->read(); 
    buff += thisChar; 
  }

  int frameshift = buff.length() - 6; 

  if(buff.length() % 6 != 0) {
    Serial.print("Bad buffer: "); 
  }
  Serial.println(buff); 

  String currentStr = ""; 
  for(int i=0; i<6; i++) {
    setRelay(i, buff.charAt(i + frameshift) == '1'); 
    currentStr += lastCurrents[i]; 
    currentStr += ","; 
  }
  client->print(currentStr); 
}

void loop() {
  EthernetClient baseClient = baseConn.available();

  if(baseClient) {
    processData(&baseClient, &baseConn);
  }
  
  for(int i=0; i<6; i++) {
    lastCurrents[i] = readCurrent(i); 
  }
  delay(10); 
}
