//L293D
//Joint Motor 1
int InA1  = 2;  
int InB1  = 3;  

//Joint Motor 2
int InA2  = 4; 
int InB2  = 5; 

//Middle Motor 3
int InA3  = 6; 
int InB3  = 7;  

//Middle Motor 4
int InA4  = 8; 
int InB4  = 9;  

//Motor speed
int Mspeed = 80;

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
    analogWrite(InB1, 0);
    analogWrite(InA1, 0);
    analogWrite(InB2, 0);
    analogWrite(InA2, 0);

    //Middle motors
    analogWrite(InB3, 0);
    analogWrite(InA3, 0);
    analogWrite(InB4, 0);
    analogWrite(InA4, 0);
}

//Pivot left
void pivotL(){
    analogWrite(InB1, Mspeed);
    analogWrite(InA1, 0);
    analogWrite(InB2, 0);
    analogWrite(InA2, Mspeed);

    //Middle motors
    analogWrite(InB3, 0);
    analogWrite(InA3, 0);
    analogWrite(InB4, 0);
    analogWrite(InA4, 0);
}

//Pivot right
void pivotR(){
    analogWrite(InB1, 0);
    analogWrite(InA1, Mspeed);
    analogWrite(InB2, Mspeed);
    analogWrite(InA2, 0);

    //Middle motors
    analogWrite(InB3, 0);
    analogWrite(InA3, 0);
    analogWrite(InB4, 0);
    analogWrite(InA4, 0);
}

void forward(){
    analogWrite(InB1, Mspeed);
    analogWrite(InA1, 0);
    analogWrite(InB2, Mspeed);
    analogWrite(InA2, 0);

    //Middle motors
    analogWrite(InB3, Mspeed);
    analogWrite(InA3, 0);
    analogWrite(InB4, 0);
    analogWrite(InA4, Mspeed);
}

void backward(){
    analogWrite(InA1, Mspeed);
    analogWrite(InB1, 0);
    
    analogWrite(InA2, Mspeed);
    analogWrite(InB2, 0);

    //Middle motors
    analogWrite(InB3, 0); 
    analogWrite(InA3, Mspeed);
    
    analogWrite(InB4, Mspeed);
    analogWrite(InA4, 0);
}

