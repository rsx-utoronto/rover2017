#include <Arduino.h>
#include <main.h>

void setup() {
    Serial.begin(9600);
    while (!Serial);
    lastUpdateTime = millis();
    pinMode(l_wrist_PIN, OUTPUT);
    pinMode(r_wrist_PIN, OUTPUT);
    pinMode(forearm_PIN, OUTPUT);
    pinMode(gripper_PIN, OUTPUT);
    pinMode(elbow_PIN, OUTPUT);
    pinMode(shoulder_PIN, OUTPUT);

    pinMode(l_wrist_DIR, OUTPUT);
    pinMode(r_wrist_DIR, OUTPUT);
    pinMode(forearm_DIR, OUTPUT);
    pinMode(gripper_DIR, OUTPUT);
    pinMode(elbow_DIR, OUTPUT);
    pinMode(shoulder_DIR, OUTPUT);
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
