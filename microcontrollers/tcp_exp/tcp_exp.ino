/*
 Echo Server

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

void setup() {
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

void processData(EthernetClient * client, EthernetServer * server){
  String buff = ""; 
  while (client->available() > 0) {
      // read the bytes incoming from the client:
      char thisChar = client->read();
      buff += thisChar; 
  }

  Serial.print("left motor "); 
  Serial.println(buff.substring(0, 5).toInt()); 

  Serial.print("right motor "); 
  Serial.println(buff.substring(5, 10).toInt()); 

  Serial.print("pivot "); 
  Serial.println(buff.substring(10, 14).toInt()); 

  Serial.print("drive mode "); 
  Serial.println(buff.charAt(14)); 
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



