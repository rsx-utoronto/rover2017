//L293D
//Joint Right Motors
int InA1  = 2;  
int InB1  = 4;  

//Joint Left Motors
int InA2  = 7; 
int InB2  = 8; 

//Middle Right Motor 
int InA3  = 10; 
int InB3  = 11;  

//Middle Left Motor 
int InA4  = 12; 
int InB4  = 13;  

//Motor speed
int Mspeed = 80;

//PWM enable pins
//Right motor
int En1 = 3;
//Left motor
int En2 = 5;
//Middle right motor
int En3 = 6;
//Middle left motor
int En4 = 9;

void setup(){
 
    //Set pins as outputs
    pinMode(InA1, OUTPUT);
    pinMode(InA2, OUTPUT);
    pinMode(InA3, OUTPUT);
    pinMode(InA4, OUTPUT);
    pinMode(InB1, OUTPUT);
    pinMode(InB2, OUTPUT);
    pinMode(InB3, OUTPUT);
    pinMode(InB4, OUTPUT);

}

void loop() {
  //Testing
  forward();
  delay(5000); 
  backward();
  delay(5000); 
  pivotR();
  delay(5000);
  pivotL();
  delay(5000);
  Mstop();
}

//Stop the motor
void Mstop(){
    digitalWrite(InB1, 0);
    digitalWrite(InA1, 0);
    digitalWrite(InB2, 0);
    digitalWrite(InA2, 0);

    //Middle motors
    digitalWrite(InB3, 0);
    digitalWrite(InA3, 0);
    digitalWrite(InB4, 0);
    digitalWrite(InA4, 0);
}

//Pivot left
void pivotL(){
    digitalWrite(InB1, Mspeed);
    digitalWrite(InA1, 0);
    digitalWrite(InB2, 0);
    digitalWrite(InA2, Mspeed);

    //Middle motors
    digitalWrite(InB3, 0);
    digitalWrite(InA3, 0);
    digitalWrite(InB4, 0);
    digitalWrite(InA4, 0);
}

//Pivot right
void pivotR(){
    digitalWrite(InB1, 0);
    digitalWrite(InA1, Mspeed);
    digitalWrite(InB2, Mspeed);
    digitalWrite(InA2, 0);

    //Middle motors
    digitalWrite(InB3, 0);
    digitalWrite(InA3, 0);
    digitalWrite(InB4, 0);
    digitalWrite(InA4, 0);
}

void forward(){
    digitalWrite(InB1, Mspeed);
    digitalWrite(InA1, 0);
    digitalWrite(InB2, Mspeed);
    digitalWrite(InA2, 0);

    //Middle motors
    digitalWrite(InB3, Mspeed);
    digitalWrite(InA3, 0);
    digitalWrite(InB4, 0);
    digitalWrite(InA4, Mspeed);
}

void backward(){
    digitalWrite(InA1, Mspeed);
    digitalWrite(InB1, 0);
    
    digitalWrite(InA2, Mspeed);
    digitalWrite(InB2, 0);

    //Middle motors
    digitalWrite(InB3, 0); 
    digitalWrite(InA3, Mspeed);
    
    digitalWrite(InB4, Mspeed);
    digitalWrite(InA4, 0);
}

