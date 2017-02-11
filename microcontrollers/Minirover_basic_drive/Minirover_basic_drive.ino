//L293D
//Joint Motor 1
int inA1  = 2;
int inB1  = 3;

//Joint Motor 2
int inA2  = 4;
int inB2  = 5;

//Middle Motor 3
int inA3  = 6;
int inB3  = 7;

//Middle Motor 4
int inA4  = 8;
int inB4  = 9;

//Motor speed
int mSpeed = 150;

void setup() {
    //Set pins as outputs
    pinMode(inA1, OUTPUT);
    pinMode(inA2, OUTPUT);
    pinMode(inA3, OUTPUT);
    pinMode(inA4, OUTPUT);
    pinMode(inB1, OUTPUT);
    pinMode(inB2, OUTPUT);
    pinMode(inB3, OUTPUT);
    pinMode(inB4, OUTPUT);
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
    analogWrite(inB1, 0);
    analogWrite(inA1, 0);
    analogWrite(inB2, 0);
    analogWrite(inA2, 0);

    //Middle motors
    analogWrite(inB3, 0);
    analogWrite(inA3, 0);
    analogWrite(inB4, 0);
    analogWrite(inA4, 0);
}

//Pivot left
void pivotL(){
    analogWrite(inB1, mSpeed);
    analogWrite(inA1, 0);
    analogWrite(inB2, 0);
    analogWrite(inA2, mSpeed);

    //Middle motors
    analogWrite(inB3, 0);
    analogWrite(inA3, 0);
    analogWrite(inB4, 0);
    analogWrite(inA4, 0);
}

//Pivot right
void pivotR(){
    analogWrite(inB1, 0);
    analogWrite(inA1, mSpeed);
    analogWrite(inB2, mSpeed);
    analogWrite(inA2, 0);

    //Middle motors
    analogWrite(inB3, 0);
    analogWrite(inA3, 0);
    analogWrite(inB4, 0);
    analogWrite(inA4, 0);
}

void forward(){
    analogWrite(inB1, mSpeed);
    analogWrite(inA1, 0);
    analogWrite(inB2, mSpeed);
    analogWrite(inA2, 0);

    //Middle motors
    analogWrite(inB3, mSpeed);
    analogWrite(inA3, 0);
    analogWrite(inB4, 0);
    analogWrite(inA4, mSpeed);
}

void backward(){
    analogWrite(inA1, mSpeed);
    analogWrite(inB1, 0);

    analogWrite(inA2, mSpeed);
    analogWrite(inB2, 0);

    //Middle motors
    analogWrite(inB3, 0);
    analogWrite(inA3, mSpeed);

    analogWrite(inB4, mSpeed);
    analogWrite(inA4, 0);
}

