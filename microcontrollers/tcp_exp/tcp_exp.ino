/*
 Chat Server

 A simple server that distributes any incoming messages to all
 connected clients.  To use, telnet to your device's IP address and type.
 You can see the client's input in the serial monitor as well.
 Using an Arduino Wiznet Ethernet shield.

RSX: connect using Node server or any TCP connection. Use port numbers specifed below to connect. 
Supports two connections, one for Base Station Node server, other for autnomous software

 Circuit:
 * Ethernet shield attached to pins 10, 11, 12, 13

 created 18 Dec 2009
 by David A. Mellis
 modified 9 Apr 2012
 by Tom Igoe

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
#define AutoSysPort 6000

EthernetServer baseConn(baseStationPort);
EthernetServer AutoSysConn(AutoSysPort);

void setup() {
  // initialize the ethernet device
  Ethernet.begin(mac, ip, myDns, gateway, subnet);
  // start listening for clients
  baseConn.begin();
  AutoSysConn.begin();
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }


  Serial.print("IP address:");
  Serial.println(Ethernet.localIP());
}

void processData(EthernetClient * client, short AutoSysOrBase){
  while (client->available() > 0) {
      // read the bytes incoming from the client:
      char thisChar = client->read();
      // echo the bytes back to the client:
      if(AutoSysOrBase)
        baseConn.write(thisChar);
       else
          AutoSysConn.write(thisChar);
          // echo the bytes to the server as well:
      Serial.write(thisChar);
    }
}

void loop() {
  // wait for a new client:
  EthernetClient baseClient = baseConn.available();
  EthernetClient autoSysClient = AutoSysConn.available();
  

  if(autoSysClient){
     processData(&autoSysClient, 0);
  }
  
   else if(baseClient) {
//    if (!alreadyConnected) {
//      // clear out the input buffer:
//      baseClient.flush();
//      Serial.println("Connected to Node Server");
//      baseClient.println("Arduino: Welcome to the Jungle ");
//      alreadyConnected = true;
//    }

     processData(&baseClient, 1);
    
  }

  //client.println("C FTW!");
//  server.write("I hate js\n");
}



