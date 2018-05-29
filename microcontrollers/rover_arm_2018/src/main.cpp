#include <Arduino.h>
#include <Stream.h>
#include <PID_v1.h>
// #include <digitalWriteFast.h>
#include <main.h>

// change to REVERSE if needed
PID PID_0(&actual_pos_float[0], &vel[0], &goal_pos[0], Kp[0], Ki[0], Kd[0], DIRECT);
PID PID_1(&actual_pos_float[1], &vel[1], &goal_pos[1], Kp[1], Ki[1], Kd[1], DIRECT);
PID PID_2(&actual_pos_float[2], &vel[2], &goal_pos[2], Kp[2], Ki[2], Kd[2], DIRECT);
PID PID_3(&actual_pos_float[3], &vel[3], &goal_pos[3], Kp[3], Ki[3], Kd[3], REVERSE);
PID PID_4(&actual_pos_float[4], &vel[4], &goal_pos[4], Kp[4], Ki[4], Kd[4], DIRECT);
PID PID_5(&actual_pos_float[5], &vel[5], &goal_pos[5], Kp[5], Ki[5], Kd[5], REVERSE);
PID PID_6(&actual_pos_float[6], &vel[6], &goal_pos[6], Kp[6], Ki[6], Kd[6], REVERSE);

void setup() {
    Serial.begin(115200);
    while (!Serial)
        ;
    Serial.setTimeout(2);
    Serial.println("Serial initialized.");
    drivers_initilize();
    setup_interrupts();
    setup_PID();
    Serial.println("drivers and encoders initialized.");
}

unsigned long last_print = millis();

void loop() {
    int last_override;

    if (Serial.available()) {
        switch (Serial.read()) {
            case 'p': // limited absolute
                // there should be a space, discard it.
                Serial.read();
                update_goals(false, true);
                break;
            case 'f': // No limit absolute
                Serial.read();
                update_goals(true, true);
                break;
            case 'r': // no limit relative
                Serial.read();
                update_goals(true, false);
                break;
            case 'e': // e-stop
                running = 0;
                break;
            case 'c': // continue operation
                running = 1;
                // update PID twice so D term does not explode
                updatePID();
                break;
            case 'z': // zero out encoders
                for (int i = 0; i < 7; i++) {
                    actual_pos[i] = 0;
                    goal_pos[i] = 0;
                }
                // update PID twice so D term does not explode
                updatePID();
                break;
            case 'm':
                last_override = millis();
                manual_override = true;
                break;
            case 's': // starting position (fully upright and center)
                // shoulder rotation centered
                actual_pos[0] = 0;
                goal_pos[0] = 0;
                // shoulder and elbow fully upright
                actual_pos[1] = high_pos_limit[1];
                goal_pos[1] = high_pos_limit[1];
                actual_pos[2] = high_pos_limit[2];
                goal_pos[2] = high_pos_limit[2];
                for (int i = 3; i <= 6; i++){
                    actual_pos[i] = 0;
                    goal_pos[i] = 0;
                }
                // update PID twice so D term does not explode
                updatePID();
                break;
            case 'a': // print encoder positions
                PRINT_encoder_positions();
                break;
            default:
                Serial.println("parse err");
        }
    }
    if (manual_override) {
        if (running) {

        } else {

        }
    } else {
        updatePID();
        update_velocity();
    }
}

void updatePID() {
    actual_pos_float[0] = (double) actual_pos[0];
    PID_0.Compute();
    actual_pos_float[1] = (double) actual_pos[1];
    PID_1.Compute();
    actual_pos_float[2] = (double) actual_pos[2];
    PID_2.Compute();
    actual_pos_float[3] = (double) actual_pos[3];
    PID_3.Compute();
    actual_pos_float[4] = (double) actual_pos[4];
    PID_4.Compute();
    actual_pos_float[5] = (double) actual_pos[5];
    PID_5.Compute();
    actual_pos_float[6] = (double) actual_pos[6];
    PID_6.Compute();
}

void update_goals(bool no_limits = false, bool absolute = true) {
    // disable manual override
    manual_override = false;

    int raw_pos[7];
    for (int i = 0; i < 7; i++) {
        // Parse incoming integer. raw_pos holds the angles of the IK model.
        // These angles will be translated to output joints so that the
        // differential spherical wrist and gripper can operate
        raw_pos[i] = Serial.parseInt();
        // apply constraints at raw joint angle level (if applicable)
        if (!no_limits) {
            raw_pos[i] = constrain(raw_pos[i], low_pos_limit[i], high_pos_limit[i]);
        }
    }
    if (absolute) {
        goal_pos[0] = raw_pos[0];
        goal_pos[1] = -raw_pos[1];
        goal_pos[2] = raw_pos[2];
        goal_pos[3] = -raw_pos[3];
        // Translate IK spherical model to differential wrist
        goal_pos[4] = - raw_pos[4] + raw_pos[5];  // tilt + rot
        goal_pos[5] = - raw_pos[4] - raw_pos[5]; // tilt + rot
        // Take into account spherical wrist rotation for the gripper output
        goal_pos[6] = raw_pos[6] - ((double) raw_pos[5] * 1680.0/(26.9*64.0));
    } else {
        // RELATIVE mode, just add the values.
        goal_pos[0] += raw_pos[0];
        goal_pos[1] += -raw_pos[1];
        goal_pos[2] += raw_pos[2];
        goal_pos[3] += -raw_pos[3];
        // Translate IK spherical model to differential wrist
        goal_pos[4] += - raw_pos[4] + raw_pos[5];  // tilt + rot
        goal_pos[5] += - raw_pos[4] - raw_pos[5]; // tilt + rot
        // Take into account spherical wrist rotation for the gripper output
        goal_pos[6] += raw_pos[6] - ((double) raw_pos[5] * 1680.0/(26.9*64.0));
    }
    // TESTING
    for (int i = 0; i < 7; i++) {
        Serial.print(goal_pos[i]);
        Serial.print(' ');
    }
    PRINT_encoder_positions();
}

void update_velocity() {
    for (int i = 0; i < 7; i++) {
        if (running) {
            digitalWrite(dirPin[i], vel[i] > 0);
            analogWrite(pwmPin[i], abs(vel[i]));
        } else {
            analogWrite(pwmPin[i], 0);
        }
    }
}

void drivers_initilize() {
    for (int i = 0; i < 7; i++) {
        pinMode(dirPin[i], OUTPUT);
        pinMode(pwmPin[i], OUTPUT);
    }
}

void setup_interrupts() {
    for(int i = 0; i < 7; i++) {
        pinMode(enc_A[i], INPUT);
        pinMode(enc_B[i], INPUT);
    }
    // same with 
    attachInterrupt(digitalPinToInterrupt(enc_A[0]), A0_handler, CHANGE);
    attachInterrupt(digitalPinToInterrupt(enc_B[0]), B0_handler, CHANGE);
    attachInterrupt(digitalPinToInterrupt(enc_A[1]), A1_handler, CHANGE);
    attachInterrupt(digitalPinToInterrupt(enc_B[1]), B1_handler, CHANGE);
    attachInterrupt(digitalPinToInterrupt(enc_A[2]), A2_handler, CHANGE);
    attachInterrupt(digitalPinToInterrupt(enc_B[2]), B2_handler, CHANGE);
    attachInterrupt(digitalPinToInterrupt(enc_A[3]), A3_handler, CHANGE);
    attachInterrupt(digitalPinToInterrupt(enc_B[3]), B3_handler, CHANGE);
    attachInterrupt(digitalPinToInterrupt(enc_A[4]), A4_handler, CHANGE);
    attachInterrupt(digitalPinToInterrupt(enc_B[4]), B4_handler, CHANGE);
    attachInterrupt(digitalPinToInterrupt(enc_A[5]), A5_handler, CHANGE);
    attachInterrupt(digitalPinToInterrupt(enc_B[5]), B5_handler, CHANGE);
    attachInterrupt(digitalPinToInterrupt(enc_A[6]), A6_handler, CHANGE);
    attachInterrupt(digitalPinToInterrupt(enc_B[6]), B6_handler, CHANGE);
}

void setup_PID(){
    PID_0.SetMode(AUTOMATIC);
    PID_0.SetOutputLimits(-spdLimit[0], spdLimit[0]);
    PID_1.SetMode(AUTOMATIC);
    PID_1.SetOutputLimits(-spdLimit[1], spdLimit[1]);
    PID_2.SetMode(AUTOMATIC);
    PID_2.SetOutputLimits(-spdLimit[2], spdLimit[2]);
    PID_3.SetMode(AUTOMATIC);
    PID_3.SetOutputLimits(-spdLimit[3], spdLimit[3]);
    PID_4.SetMode(AUTOMATIC);
    PID_4.SetOutputLimits(-spdLimit[4], spdLimit[4]);
    PID_5.SetMode(AUTOMATIC);
    PID_5.SetOutputLimits(-spdLimit[5], spdLimit[5]);
    PID_6.SetMode(AUTOMATIC);
    PID_6.SetOutputLimits(-spdLimit[6], spdLimit[6]);
}

void A0_handler() {
    if (digitalRead(enc_A[0])) { // rising edge
        digitalRead(enc_B[0]) ? actual_pos[0]-- : actual_pos[0]++;
    } else { // falling edge
        digitalRead(enc_B[0]) ? actual_pos[0]++ : actual_pos[0]--;
    }
}

void B0_handler() {
    if (digitalRead(enc_B[0])) { // rising edge
        digitalRead(enc_A[0]) ? actual_pos[0]++ : actual_pos[0]--;
    } else { // falling edge
        digitalRead(enc_A[0]) ? actual_pos[0]-- : actual_pos[0]++;
    }
}

void A1_handler() {
    if (digitalRead(enc_A[1])) { // rising edge
        digitalRead(enc_B[1]) ? actual_pos[1]-- : actual_pos[1]++;
    } else { // falling edge
        digitalRead(enc_B[1]) ? actual_pos[1]++ : actual_pos[1]--;
    }
}

void B1_handler() {
    if (digitalRead(enc_B[1])) { // rising edge
        digitalRead(enc_A[1]) ? actual_pos[1]++ : actual_pos[1]--;
    } else { // falling edge
        digitalRead(enc_A[1]) ? actual_pos[1]-- : actual_pos[1]++;
    }
}

void A2_handler() {
    if (digitalRead(enc_A[2])) { // rising edge
        digitalRead(enc_B[2]) ? actual_pos[2]-- : actual_pos[2]++;
    } else { // falling edge
        digitalRead(enc_B[2]) ? actual_pos[2]++ : actual_pos[2]--;
    }
}

void B2_handler() {
    if (digitalRead(enc_B[2])) { // rising edge
        digitalRead(enc_A[2]) ? actual_pos[2]++ : actual_pos[2]--;
    } else { // falling edge
        digitalRead(enc_A[2]) ? actual_pos[2]-- : actual_pos[2]++;
    }
}

void A3_handler() {
    if (digitalRead(enc_A[3])) { // rising edge
        digitalRead(enc_B[3]) ? actual_pos[3]-- : actual_pos[3]++;
    } else { // falling edge
        digitalRead(enc_B[3]) ? actual_pos[3]++ : actual_pos[3]--;
    }
}

void B3_handler() {
    if (digitalRead(enc_B[3])) { // rising edge
        digitalRead(enc_A[3]) ? actual_pos[3]++ : actual_pos[3]--;
    } else { // falling edge
        digitalRead(enc_A[3]) ? actual_pos[3]-- : actual_pos[3]++;
    }
}

void A4_handler() {
    if (digitalRead(enc_A[4])) { // rising edge
        digitalRead(enc_B[4]) ? actual_pos[4]-- : actual_pos[4]++;
    } else { // falling edge
        digitalRead(enc_B[4]) ? actual_pos[4]++ : actual_pos[4]--;
    }
}

void B4_handler() {
    if (digitalRead(enc_B[4])) { // rising edge
        digitalRead(enc_A[4]) ? actual_pos[4]++ : actual_pos[4]--;
    } else { // falling edge
        digitalRead(enc_A[4]) ? actual_pos[4]-- : actual_pos[4]++;
    }
}

void A5_handler() {
    if (digitalRead(enc_A[5])) { // rising edge
        digitalRead(enc_B[5]) ? actual_pos[5]-- : actual_pos[5]++;
    } else { // falling edge
        digitalRead(enc_B[5]) ? actual_pos[5]++ : actual_pos[5]--;
    }
}

void B5_handler() {
    if (digitalRead(enc_B[5])) { // rising edge
        digitalRead(enc_A[5]) ? actual_pos[5]++ : actual_pos[5]--;
    } else { // falling edge
        digitalRead(enc_A[5]) ? actual_pos[5]-- : actual_pos[5]++;
    }
}

void A6_handler() {
    if (digitalRead(enc_A[6])) { // rising edge
        digitalRead(enc_B[6]) ? actual_pos[6]-- : actual_pos[6]++;
    } else { // falling edge
        digitalRead(enc_B[6]) ? actual_pos[6]++ : actual_pos[6]--;
    }
}

void B6_handler() {
    if (digitalRead(enc_B[6])) { // rising edge
        digitalRead(enc_A[6]) ? actual_pos[6]++ : actual_pos[6]--;
    } else { // falling edge
        digitalRead(enc_A[6]) ? actual_pos[6]-- : actual_pos[6]++;
    }
}

// Testing functions
void TEST_find_encoder_pins() {
    while(true){
        for(int i = 2; i <= 53; i++){
            pinMode(i, INPUT);
        }
        for(int i = 2; i <= 53; i++){
            Serial.print(i);
            Serial.print(digitalRead(i) ? 'X' : ' ');
            Serial.print(' ');
        }
        Serial.println();
    }
}

void TEST_print_encoder_pins(){
    for(int i = 0; i < 7; i++) {
        pinMode(enc_A[i], INPUT);
        pinMode(enc_B[i], INPUT);
    }
    while(true){
        Serial.print("A: ");
        for(int i = 0; i < 7; i++) {
            Serial.print(digitalRead(enc_A[i]));
        }
        Serial.print(" B: ");
        for(int i = 0; i < 7; i++) {
            Serial.print(digitalRead(enc_B[i]));
        }
        Serial.println();
    }
}

void PRINT_encoder_positions(){
    Serial.print("Encoders: ");
    for(int i = 0; i < 7; i++){
        Serial.print(actual_pos[i]);
        Serial.print(' ');
    }
    Serial.println();
}

void TEST_PID(){
    unsigned long last_goal_change = millis();
    for(int i = 0; i < 7; i++){
        goal_pos[i] = 1000;
    }
    while(true) {
        // change goal ever second for testing
        if(millis() - last_goal_change > 1000){
            for(int i = 0; i < 7; i++){
                goal_pos[i] = -goal_pos[i];
            }
            last_goal_change = millis();
        }
        Serial.println("goal: ");
        Serial.print(goal_pos[0]);
        Serial.print(" actual_pos: ");
        for(int i = 0; i < 7; i++){
            Serial.print(actual_pos[i]);
            Serial.print(' ');
        }
        Serial.print(" vel: ");
        updatePID();
        for(int i = 0; i < 7; i++){
            Serial.print(vel[i]);
            Serial.print(' ');
        }
        Serial.println();
    }
}

void TEST_motor_pins(){
    while(true){
        for(int i = 0; i < 7; i++) {
            Serial.println(i);
            // forwards
            digitalWrite(dirPin[i], 0);
            analogWrite(pwmPin[i], spdLimit[i]);
            delay(200);
            // stop
            analogWrite(pwmPin[i], 0);
            delay(1000);
            // back
            digitalWrite(dirPin[i], 1);
            analogWrite(pwmPin[i], spdLimit[i]);
            delay(200);
            // stop
            analogWrite(pwmPin[i], 0);
            delay(3000);
        }
    }
}

void PRINT_oscilloscope(int motor){
    if (millis() - last_print > 15) {
        int x = actual_pos[motor];
        for (int i = 0; i < 200; i++){
            if (i == goal_pos[motor]){
                Serial.print('|');
            } else if (i == x) {
                Serial.print('#');
            } else {
                Serial.print(' ');
            }
        }
        last_print = millis();
        Serial.println(last_print);
    }
}
