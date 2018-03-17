#include <Arduino.h>
#include <main.h>

void setup() {
    Serial.begin(9600);
    while (!Serial);
    lastUpdateTime = millis();
    pinMode(l_wrist_pin, OUTPUT);
    pinMode(r_wrist_pin, OUTPUT);
    pinMode(forearm_pin, OUTPUT);
    pinMode(gripper_pin, OUTPUT);
    pinMode(elbow_pin, OUTPUT);
    pinMode(shoulder_pin, OUTPUT);
}

void loop() {
    if (millis() - lastUpdateTime > 500) {
        stopAllMotors();
    }

    if (Serial.available() > 0) {
        uint8_t inByte = Serial.read();
        setVariables(inByte);
        updateMotors();
        lastUpdateTime = millis();
    }
}