#include <Arduino.h>
#include <main.h>
#include <PID_v1.h>
#include <digitalWriteFast.h>

PID PID_0(&actual_pos[0], &vel[0], &goal_pos[0], Kp[0], Ki[0], Kd[0], DIRECT);
PID PID_1(&actual_pos[1], &vel[1], &goal_pos[1], Kp[1], Ki[1], Kd[1], DIRECT);
PID PID_2(&actual_pos[2], &vel[2], &goal_pos[2], Kp[2], Ki[2], Kd[2], DIRECT);
PID PID_3(&actual_pos[3], &vel[3], &goal_pos[3], Kp[3], Ki[3], Kd[3], DIRECT);
PID PID_4(&actual_pos[4], &vel[4], &goal_pos[4], Kp[4], Ki[4], Kd[4], DIRECT);
PID PID_5(&actual_pos[5], &vel[5], &goal_pos[5], Kp[5], Ki[5], Kd[5], DIRECT);
PID PID_6(&actual_pos[6], &vel[6], &goal_pos[6], Kp[6], Ki[6], Kd[6], DIRECT);

void setup() {
    Serial.begin(115200);
    while (!Serial);
    Serial.setTimeout(2);
    drivers_initilize();
    setup_interrupts();
}

void loop() {
    if(Serial.available()){
        switch(Serial.read();) {
            case 'p': // goal position update
                update_goals();
                break;
            case 'e': // e-stop
                running = 0;
                break;
            case 'r': // resume operation
                running = 1;
                break;
            case 'z': // zero out encoders
                for(int i = 0; i < 7; i++){
                    actual_pos[i] = 0;
                    goal_pos[0] = 0;
                }
                break;
        default:
            Serial.println("parse err");
        }
    }
    updatePID();
    update_velocity();
}

void updatePID(){
    PID_0.Compute();
    PID_1.Compute();
    PID_2.Compute();
    PID_3.Compute();
    PID_4.Compute();
    PID_5.Compute();
    PID_6.Compute();
}

void update_goals(){
    int raw_pos [7];
    for(int i = 0; i < 7; i++){
        // parse incoming integer
        raw_pos[i] = Serial.parseInt(' ');
        // apply constraints at raw joint angle level
        raw_pos[i] = constrain(raw_pos[i], low_pos_limit[i], high_pos_limit[i]);
    }
    for(int i = 0; i <= 3; i++){
        // 0-3 joints translate directly
        goal_pos[i] = raw_pos[i];
    }
    // Translate IK spherical model to differential wrist
    goal_pos[4] = raw_pos[4] + raw_pos[5]; // tilt + rot
    goal_pos[5] = - raw_pos[4] + raw_pos[5]; // - til + rot
    // Gripper position must take into account spherical wrist rotaiton
    goal_pos[6] = raw_pos[6] - (int) ((float) raw_pos[5] * 1.0) ;
}

void update_velocity(){
        for(int i = 0; i < 7; i++){
            if(running) {
                digitalWrite(dirPin[i], sign(shoulder_vel));
                analogWrite(pwmPin[i], min(abs(shoulder_vel), spdLimit[i]));
            } else {
                analogWrite(pwmPin[i], 0);
            }
        }
    }
}

void drivers_initilize(){
    for(int i = 0; i < 7; i++){
        pinMode(dirPin[i], OUTPUT);
        pinMode(pwmPin[i], OUTPUT);
    }
}

void setup_interrupts() {
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

void A0_handler() {
    if (digitalReadFast(enc_A[0])) { //rising edge
        digitalReadFast(enc_B[0]) ? actual_pos[0]-- : actual_pos[0]++;
    } else { //falling edge
        digitalReadFast(enc_B[0]) ? actual_pos[0]++ : actual_pos[0]--;
  }
}

void B0_handler() {
  if (digitalReadFast(enc_B[0])) { //rising edge
    digitalReadFast(enc_A[0]) ? actual_pos[0]++ : actual_pos[0]--;
  } else { //falling edge
    digitalReadFast(enc_A[0]) ? actual_pos[0]-- : actual_pos[0]++;
  }
}

void A1_handler() {
    if (digitalReadFast(enc_A[1])) { //rising edge
        digitalReadFast(enc_B[1]) ? actual_pos[1]-- : actual_pos[1]++;
    } else { //falling edge
        digitalReadFast(enc_B[1]) ? actual_pos[1]++ : actual_pos[1]--;
  }
}

void B1_handler() {
  if (digitalReadFast(enc_B[1])) { //rising edge
    digitalReadFast(enc_A[1]) ? actual_pos[1]++ : actual_pos[1]--;
  } else { //falling edge
    digitalReadFast(enc_A[1]) ? actual_pos[1]-- : actual_pos[1]++;
  }
}

void A2_handler() {
    if (digitalReadFast(enc_A[2])) { //rising edge
        digitalReadFast(enc_B[2]) ? actual_pos[2]-- : actual_pos[2]++;
    } else { //falling edge
        digitalReadFast(enc_B[2]) ? actual_pos[2]++ : actual_pos[2]--;
  }
}

void B2_handler() {
  if (digitalReadFast(enc_B[2])) { //rising edge
    digitalReadFast(enc_A[2]) ? actual_pos[2]++ : actual_pos[2]--;
  } else { //falling edge
    digitalReadFast(enc_A[2]) ? actual_pos[2]-- : actual_pos[2]++;
  }
}

void A3_handler() {
    if (digitalReadFast(enc_A[3])) { //rising edge
        digitalReadFast(enc_B[3]) ? actual_pos[3]-- : actual_pos[3]++;
    } else { //falling edge
        digitalReadFast(enc_B[3]) ? actual_pos[3]++ : actual_pos[3]--;
  }
}

void B3_handler() {
  if (digitalReadFast(enc_B[3])) { //rising edge
    digitalReadFast(enc_A[3]) ? actual_pos[3]++ : actual_pos[3]--;
  } else { //falling edge
    digitalReadFast(enc_A[3]) ? actual_pos[3]-- : actual_pos[3]++;
  }
}

void A4_handler() {
    if (digitalReadFast(enc_A[4])) { //rising edge
        digitalReadFast(enc_B[4]) ? actual_pos[4]-- : actual_pos[4]++;
    } else { //falling edge
        digitalReadFast(enc_B[4]) ? actual_pos[4]++ : actual_pos[4]--;
  }
}

void B4_handler() {
  if (digitalReadFast(enc_B[4])) { //rising edge
    digitalReadFast(enc_A[4]) ? actual_pos[4]++ : actual_pos[4]--;
  } else { //falling edge
    digitalReadFast(enc_A[4]) ? actual_pos[4]-- : actual_pos[4]++;
  }
}

void A5_handler() {
    if (digitalReadFast(enc_A[5])) { //rising edge
        digitalReadFast(enc_B[5]) ? actual_pos[5]-- : actual_pos[5]++;
    } else { //falling edge
        digitalReadFast(enc_B[5]) ? actual_pos[5]++ : actual_pos[5]--;
  }
}

void B5_handler() {
  if (digitalReadFast(enc_B[5])) { //rising edge
    digitalReadFast(enc_A[5]) ? actual_pos[5]++ : actual_pos[5]--;
  } else { //falling edge
    digitalReadFast(enc_A[5]) ? actual_pos[5]-- : actual_pos[5]++;
  }
}

void A6_handler() {
    if (digitalReadFast(enc_A[6])) { //rising edge
        digitalReadFast(enc_B[6]) ? actual_pos[6]-- : actual_pos[6]++;
    } else { //falling edge
        digitalReadFast(enc_B[6]) ? actual_pos[6]++ : actual_pos[6]--;
  }
}

void B6_handler() {
  if (digitalReadFast(enc_B[6])) { //rising edge
    digitalReadFast(enc_A[6]) ? actual_pos[6]++ : actual_pos[6]--;
  } else { //falling edge
    digitalReadFast(enc_A[6]) ? actual_pos[6]-- : actual_pos[6]++;
  }
}
