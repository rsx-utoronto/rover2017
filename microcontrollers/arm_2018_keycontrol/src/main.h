#include <Arduino.h>

const uint8_t l_wrist_PIN = 5;
const uint8_t l_wrist_DIR = 24;
const uint8_t r_wrist_PIN = 6;
const uint8_t r_wrist_DIR = 32;
const uint8_t forearm_PIN = 7;
const uint8_t forearm_DIR = 42;
const uint8_t gripper_PIN = 4;
const uint8_t gripper_DIR = 40;
const uint8_t elbow_PIN = 3;
const uint8_t elbow_DIR = 38;
const uint8_t shoulder_PIN = 2;
const uint8_t shoulder_DIR = 34;


int16_t motorSpeed = 80;
int16_t l_wrist_vel = 0;
int16_t r_wrist_vel = 0;
int16_t forearm_vel = 0;
int16_t gripper_vel = 0;
int16_t elbow_vel = 0;
int16_t shoulder_vel = 0;
uint32_t lastUpdateTime = 0;

// Keymaps
// Control Signals
const uint8_t KEEP_ALIVE = 1;
const uint8_t EMERG_STOP = 2;

// Wrist Rotate
const uint8_t W_ROT_L_A = 10;
const uint8_t W_ROT_L_X = 11;
const uint8_t W_ROT_R_A = 12;
const uint8_t W_ROT_R_X = 13;

// Wrist Pitch
const uint8_t W_PIT_U_A = 14;
const uint8_t W_PIT_U_X = 15;
const uint8_t W_PIT_D_A = 16;
const uint8_t W_PIT_D_X = 17;

// Forearm Rotation
const uint8_t F_ROT_L_A = 18;
const uint8_t F_ROT_L_X = 19;
const uint8_t F_ROT_R_A = 20;
const uint8_t F_ROT_R_X = 21;

// Gripper
const uint8_t G_ACT_C_A = 22;
const uint8_t G_ACT_C_X = 23;
const uint8_t G_ACT_O_A = 24;
const uint8_t G_ACT_O_X = 25;

// Elbow Pitch
const uint8_t E_PIT_U_A = 26;
const uint8_t E_PIT_U_X = 27;
const uint8_t E_PIT_D_A = 28;
const uint8_t E_PIT_D_X = 29;

// Shoulder Pitch
const uint8_t S_PIT_U_A = 30;
const uint8_t S_PIT_U_X = 31;
const uint8_t S_PIT_D_A = 32;
const uint8_t S_PIT_D_X = 33;

int sign(int X) {
    return (int) (X > 0); 
}

void updateMotors() {
    analogWrite(abs(l_wrist_PIN), l_wrist_vel);
    analogWrite(l_wrist_DIR, sign(l_wrist_vel));
    analogWrite(abs(r_wrist_PIN), r_wrist_vel);
    analogWrite(r_wrist_DIR, sign(r_wrist_vel));
    analogWrite(abs(forearm_PIN), forearm_vel);
    analogWrite(forearm_DIR, sign(forearm_vel));
    analogWrite(abs(gripper_PIN), gripper_vel);
    analogWrite(gripper_DIR, sign(gripper_vel));
    analogWrite(abs(elbow_PIN), elbow_vel);
    analogWrite(elbow_DIR, sign(elbow_vel));
    analogWrite(abs(shoulder_PIN), shoulder_vel);
    analogWrite(shoulder_DIR, sign(shoulder_vel));
}

void stopAllMotors() {
    l_wrist_vel = 0;
    r_wrist_vel = 0;
    forearm_vel = 0;
    gripper_vel = 0;
    elbow_vel = 0;
    shoulder_vel = 0;
    updateMotors();
}

void setVariables(uint8_t inByte) {
    switch (inByte) {
    // Control Signals
    case KEEP_ALIVE:
        // do nothing
    break;
    case EMERG_STOP:
        stopAllMotors();
    break;
    // Wrist Rotate
    case W_ROT_L_A:
        l_wrist_vel += motorSpeed;
        r_wrist_vel += motorSpeed;
    break;
    case W_ROT_L_X:
        l_wrist_vel -= motorSpeed;
        r_wrist_vel -= motorSpeed;
    break;
    case W_ROT_R_A:
        l_wrist_vel -= motorSpeed;
        r_wrist_vel -= motorSpeed;
    break;
    case W_ROT_R_X:
        l_wrist_vel += motorSpeed;
        r_wrist_vel += motorSpeed;
    break;
    // Wrist Pitch
    case W_PIT_U_A:
        l_wrist_vel += motorSpeed;
        r_wrist_vel -= motorSpeed;
    break;
    case W_PIT_U_X:
        l_wrist_vel -= motorSpeed;
        r_wrist_vel += motorSpeed;
    break;
    case W_PIT_D_A:
        l_wrist_vel -= motorSpeed;
        r_wrist_vel += motorSpeed;
    break;
    case W_PIT_D_X:
        l_wrist_vel += motorSpeed;
        r_wrist_vel -= motorSpeed;
    break;
    // Forearm Rotation
    case F_ROT_L_A:
        forearm_vel += motorSpeed; 
    break;
    case F_ROT_L_X:
        forearm_vel -= motorSpeed;
    break;
    case F_ROT_R_A:
        forearm_vel -= motorSpeed;
    break;
    case F_ROT_R_X:
        forearm_vel += motorSpeed;
    break;
    // Gripper
    case G_ACT_C_A:
        gripper_vel += motorSpeed;
    break;
    case G_ACT_C_X:
        gripper_vel -= motorSpeed;
    break;
    case G_ACT_O_A:
        gripper_vel -= motorSpeed;
    break;
    case G_ACT_O_X:
        gripper_vel += motorSpeed;
    break;
    // Elbow Pitch
    case E_PIT_U_A:
        elbow_vel += motorSpeed;
    break;
    case E_PIT_U_X:
        elbow_vel -= motorSpeed;
    break;
    case E_PIT_D_A:
        elbow_vel -= motorSpeed;
    break;
    case E_PIT_D_X:
        elbow_vel += motorSpeed;
    break;
    // Shoulder Pitch
    case S_PIT_U_A:
        shoulder_vel += motorSpeed;
    break;
    case S_PIT_U_X:
        shoulder_vel -= motorSpeed;
    break;
    case S_PIT_D_A:
        shoulder_vel -= motorSpeed;
    break;
    case S_PIT_D_X:
        shoulder_vel += motorSpeed;
    break;
    default: // UNKNOWN COMMAND, INITIATE E-STOP
        stopAllMotors();
    break;
    }
}
