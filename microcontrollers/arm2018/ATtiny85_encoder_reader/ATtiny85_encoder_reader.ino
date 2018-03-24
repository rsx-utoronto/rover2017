#include <TinyWireS.h>

#define digitalPinToInterrupt(p) ( (p) == 2 ? 0 : NOT_AN_INTERRUPT)
#define SLAVE_ADDRESS 0x4

volatile uint8_t prevA = 0;
volatile uint8_t prevB = 0;
uint8_t pinA = 1;
uint8_t pinB = 3;
//uint8_t pinI = 4;


volatile int32_t count = 0;
volatile uint8_t flag = 0;

void setup() {
  //pinMode(pinA, INPUT);
  //pinMode(pinB, INPUT);
  //pinMode(pinI, INPUT);
  TinyWireS.begin(SLAVE_ADDRESS);
  TinyWireS.onRequest(requestEvent);

  int  DDRD = DDRD & B11100011;


  
  pinMode(0, OUTPUT);

  attachInterrupt(digitalPinToInterrupt(pinA), A_handler, CHANGE);
  attachInterrupt(digitalPinToInterrupt(pinB), B_handler, CHANGE);
  // Serial.begin(9600);
}

void loop() {
  //  Serial.println(count);
  //  if(digitalRead(pinI)) flag = 1;
  //  if(flag){
  //    Serial.println("#########");
  //    flag = 0;
  //  }
  //  if (count > 100) {
  //    digitalWrite(0, HIGH);
  //  }
  TinyWireS_stop_check();
}

void A_handler() {
  if (digitalRead(pinA)) { //rising edge
    digitalRead(pinB) ? count-- : count++;

  } else { //falling edge
    digitalRead(pinB) ? count++ : count--;

  }
  //if(digitalRead(pinI)) count = 0; // SINGLE REVOLUTION MODE
  //if(digitalRead(pinI)) flag = 1;
}

void B_handler() {
  if (digitalRead(pinB)) { //rising edge
    digitalRead(pinA) ? count++ : count--;
    digitalWrite(0, HIGH);
  } else { //falling edge
    digitalRead(pinA) ? count-- : count++;
    digitalWrite(0, LOW);
  }
  //if(digitalRead(pinI)) count = 0; // SINGLE REVOLUTION MODE
  //if(digitalRead(pinI)) flag = 1;
}

void requestEvent() {
  TinyWireS.send(count);
}


