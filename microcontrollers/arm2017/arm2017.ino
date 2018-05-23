#include <AccelStepper.h>
#include <SPI.h>
#include <Ethernet.h>

#define NUM_STEPPERS  	4 // number of steppers controlled by this code 

const uint8_t w1_DIR = 24;	
const uint8_t w1_PUL = 25;
const uint8_t w1_MICROSTEPS = 2;
const int32_t w1_REV = int32_t((13.0+212.0/289.0) * float(w1_MICROSTEPS) * 200.0);
const float w1_SPD = 3.0*w1_MICROSTEPS*200;
const float w1_ACL = w1_SPD/2;

const uint8_t w2_DIR = 26;
const uint8_t w2_PUL = 27;
const uint8_t w2_MICROSTEPS = 2;
const int32_t w2_REV = int32_t((13.0+212.0/289.0) * float(w2_MICROSTEPS) * 200.0);
const float w2_SPD = 3.0*w2_MICROSTEPS*200;
const float w2_ACL = w2_SPD/2;

const uint8_t w3_DIR = 28;
const uint8_t w3_PUL = 29;
const uint8_t w3_MICROSTEPS = 2;
const int32_t w3_REV = int32_t((13.0+212.0/289.0) * float(w3_MICROSTEPS) * 200.0);
const float w3_SPD = 3.0*w2_MICROSTEPS*200;
const float w3_ACL = w3_SPD/2;

const uint8_t eb_DIR = 6;
const uint8_t eb_PUL = 7;
const uint8_t eb_MICROSTEPS = 4;
const int32_t eb_REV = int32_t((13.0+212.0/289.0) * float(eb_MICROSTEPS) * 200.0 * (72.0/122.0));
const float eb_SPD = .6*eb_MICROSTEPS*200;
const float eb_ACL = eb_SPD/2;

const uint8_t sp_DIR = 10;
const uint8_t sp_PUL = 11;
const uint8_t sp_MICROSTEPS = 2;
const int32_t sp_REV = int32_t(46.656 * float(sp_MICROSTEPS) * 200.0 * 3.2 * 3.2);
const float sp_SPD = 12*sp_MICROSTEPS*200;
const float sp_ACL = sp_SPD/2;

const uint8_t sr_DIR = 4;
const uint8_t sr_PUL = 5;
const uint8_t sr_MICROSTEPS = 2;
const int32_t sr_REV = int32_t((13.0+212.0/289.0) * float(sr_MICROSTEPS) * 200.0 * (48.0/12.0));
const float sr_SPD = 5*sr_MICROSTEPS*200;
const float sr_ACL = sr_SPD/2;


uint8_t w1flag = 0;
uint8_t w2flag = 0;
uint8_t w3flag = 0;
uint8_t ebflag = 0;
uint8_t spflag = 0;
uint8_t srflag = 0;

AccelStepper sp(AccelStepper::DRIVER, sp_PUL, sp_DIR);
AccelStepper sr(AccelStepper::DRIVER, sr_PUL, sr_DIR);
AccelStepper eb(AccelStepper::DRIVER, eb_PUL, eb_DIR);
AccelStepper w1(AccelStepper::DRIVER, w1_PUL, w1_DIR);
AccelStepper w2(AccelStepper::DRIVER, w2_PUL, w2_DIR);
AccelStepper w3(AccelStepper::DRIVER, w3_PUL, w3_DIR);

// ethernet stuff
byte mac[] = {
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED
};
IPAddress ip(192, 168, 0, 181);
IPAddress myDns(192,168,1, 1);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);

#define baseStationPort 5000
#define autoSysPort 6000

EthernetServer baseConn(baseStationPort);
EthernetServer autoSysConn(autoSysPort);

void runall(){
	w1.run();
	w2.run();
	w3.run();
	eb.run();
	sp.run();
	sr.run();

	if((w1.targetPosition() == w1.currentPosition()) && (w1flag==1)) {
		w1flag = 0;
		Serial.print("w1 moved to: ");
		Serial.print(w1.currentPosition());
		Serial.print(" Time: ");
		Serial.println((float)(millis()/1000.0));
	}
	if((w2.targetPosition() == w2.currentPosition()) && (w2flag==1)) {
		w2flag = 0;
		Serial.print("w2 moved to: ");
		Serial.print(w2.currentPosition());
		Serial.print(" Time: ");
		Serial.println((float)(millis()/1000.0));
	}
	if((w3.targetPosition() == w3.currentPosition()) && (w3flag==1)) {
		w3flag = 0;
		Serial.print("w3 moved to: ");
		Serial.print(w3.currentPosition());
		Serial.print(" Time: ");
		Serial.println((float)(millis()/1000.0));
	}
	if((eb.targetPosition() == eb.currentPosition()) && (ebflag==1)) {
		ebflag = 0;
		Serial.print("eb moved to: ");
		Serial.print(eb.currentPosition());
		Serial.print(" Time: ");
		Serial.println((float)(millis()/1000.0));
	}
	if((sp.targetPosition() == sp.currentPosition()) && (spflag==1)) {
		spflag = 0;
		Serial.print("sp moved to: ");
		Serial.print(sp.currentPosition());
		Serial.print(" Time: ");
		Serial.println((float)(millis()/1000.0));
	}
	if((sr.targetPosition() == sr.currentPosition()) && (srflag==1)) {
		srflag = 0;
		Serial.print("sr moved to: ");
		Serial.print(sr.currentPosition());
		Serial.print(" Time: ");
		Serial.println((float)(millis()/1000.0));
	}
}

void setup()
{
	Serial.begin(115200);
	sp.setMaxSpeed(sp_SPD);
	sp.setAcceleration(sp_ACL);
	sr.setMaxSpeed(sr_SPD);
	sr.setAcceleration(sr_ACL);
	eb.setMaxSpeed(eb_SPD);
	eb.setAcceleration(eb_ACL);
	w1.setMaxSpeed(w1_SPD);
	w1.setAcceleration(w1_ACL);
	w2.setMaxSpeed(w2_SPD);
	w2.setAcceleration(w2_ACL);
	w3.setMaxSpeed(w3_SPD);
	w3.setAcceleration(w3_ACL);
	Serial.println("1:w1 2:w2 3:w3 4:eb 5:sp 6:sr");
	Serial.print("REV: ");
	Serial.print(w1_REV);
	Serial.print(" ");
	Serial.print(w2_REV);
	Serial.print(" ");
	Serial.print(w3_REV);
	Serial.print(" ");
	Serial.print(eb_REV);
	Serial.print(" ");
	Serial.print(sp_REV);
	Serial.print(" ");
	Serial.println(sr_REV);
	Serial.print("SPD: ");
	Serial.print(w1_SPD);
	Serial.print(" ");
	Serial.print(w2_SPD);
	Serial.print(" ");
	Serial.print(w3_SPD);
	Serial.print(" ");
	Serial.print(eb_SPD);
	Serial.print(" ");
	Serial.print(sp_SPD);
	Serial.print(" ");
	Serial.print(sr_SPD);
	Serial.print(" SUM: ");
	Serial.println(w1_SPD+w2_SPD+w3_SPD+eb_SPD+sp_SPD+sr_SPD);
	Serial.print("t:   ");
	Serial.print(((float)w1_REV/w1_SPD)/2);
	Serial.print(" ");
	Serial.print(((float)w2_REV/w2_SPD)/2);
	Serial.print(" ");
	Serial.print(((float)w3_REV/w3_SPD)/2);
	Serial.print(" ");
	Serial.print(((float)eb_REV/eb_SPD)/2);
	Serial.print(" ");
	Serial.print(((float)sp_REV/sp_SPD)/2);
	Serial.print(" ");
	Serial.println(((float)sr_REV/sr_SPD)/2);
}

// Ethernet helper function
// Takes data in {1 char flag}{10 char int}{10 char int}{10 char int}{10 char int}, total length 41 chars
void processData(EthernetClient * client, EthernetServer * server){
  	String buff = "";
  	while (client->available() > 0) {
      	// read the bytes incoming from the client:
      	char thisChar = client->read();
      	buff += thisChar;
  	}	

  	if(buff.length() % NUM_STEPPERS * 10 + 1 != 0) {
   		Serial.print("bad buffer: "); // this should never happen lol
		Serial.print(buff.length());
  	}
  	Serial.println(buff);

  	int frameshift = buff.length() - NUM_STEPPERS * 10 - 1; 

  	unsigned int inp[NUM_STEPPERS]; 
  	for(int i=0; i<NUM_STEPPERS; i++) {
  		inp[i] = buff.substring(frameshift + i * 10, frameshift + i * 10 + 10).toInt(); 
  	}
  	char mode = buff.charAt(frameshift + NUM_STEPPERS * 10);

  	switch(mode){
  		case 'p': // sets the position of each stepper
  			w1.moveTo(inp[0]); 
  			w2.moveTo(inp[1]);
  			w3.moveTo(inp[2]);
  			eb.moveTo(inp[3]);
  			// sp.moveTo(inp[4]);
  			// sr.moveTo(inp[5]);
  			w1flag = w2flag = w3flag = ebflag = spflag = srflag; 
  			break;

  		// todo [hudson]: implement your speed things here 
  		default: 
  			Serial.println("unknown flag");  // this shouldn't happen 
  	}
}

void loop()
{
	EthernetClient baseClient = baseConn.available();
  	EthernetClient autoSysClient = autoSysConn.available();

  	if(autoSysClient){
	  	processData(&autoSysClient, &autoSysConn);
	}

	else if(baseClient) {
	  	processData(&baseClient, &baseConn);
	}
	delay(10);

	Serial.print("goals: ");
	Serial.print(w1.targetPosition());
	Serial.print(" ");
	Serial.print(w2.targetPosition());
	Serial.print(" ");
	Serial.print(w3.targetPosition());
	Serial.print(" ");
	Serial.print(eb.targetPosition());
	Serial.print(" ");
	Serial.print(sp.targetPosition());
	Serial.print(" ");
	Serial.print(sr.targetPosition());
	Serial.print(" Time: ");
	Serial.println((float)(millis()/1000.0));
	runall();
}
