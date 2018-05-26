#ifndef main_h
#define main_h

double low_pos_limit[7] = {-1000000, -1000000, -1000000, -1000000, -1000000, -1000000, -1000000};
double high_pos_limit[7] = {1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000};

double goal_pos[7] = {0, 0, 0, 0, 0, 0, 0};            // position vector
volatile int actual_pos[7] = {0, 0, 0, 0, 0, 0, 0}; // actual position vector
double actual_pos_float[7] = {0, 0, 0, 0, 0, 0, 0};
double vel[7] = {0, 0, 0, 0, 0, 0, 0};

double Kp[7] = {0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5};
double Ki[7] = {0, 0, 0, 0, 0, 0, 0};
double Kd[7] = {0, 0, 0, 0, 0, 0, 0};

const char dirPin[7] = {12, 10, 13, 9, 11, 15, 14};
const char pwmPin[7] = {7, 5, 8, 4, 6, 2, 3};

const char spdLimit[7] = {255, 255, 255, 60, 60, 60, 255};
const bool reversed[7] = {0, 0, 0, 0, 0, 0, 0};

bool running = true;

const char enc_A[7] = {38, 24, 21, 32, 46, 52, 34};
const char enc_B[7] = {44, 26, 20, 48, 50, 42, 30};

void updatePID();
void drivers_initilize();
void update_velocity();
void update_encoders();
void update_goals();
void setup_interrupts();
void setup_PID();

void A0_handler();
void B0_handler();
void A1_handler();
void B1_handler();
void A2_handler();
void B2_handler();
void A3_handler();
void B3_handler();
void A4_handler();
void B4_handler();
void A5_handler();
void B5_handler();
void A6_handler();
void B6_handler();

void TEST_find_encoder_pins();
void TEST_print_encoder_pins();
void TEST_encoder_positions();
void TEST_PID();
void TEST_motor_pins();
#endif
