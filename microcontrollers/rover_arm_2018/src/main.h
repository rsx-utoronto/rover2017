#ifndef main_h
#define main_h

double low_pos_limit[7] = {-1000000, -1000000, -1000000, -1000000, -1000000, -1000000, -1000000};
double high_pos_limit[7] = {-1000000, -1000000, -1000000, -1000000, -1000000, -1000000, -1000000};

double goal_pos[7] = {0, 0, 0, 0, 0, 0, 0};            // position vector
volatile int actual_pos[7] = {0, 0, 0, 0, 0, 0, 0}; // actual position vector
double actual_pos_float[7] = {0, 0, 0, 0, 0, 0, 0};
double vel[7] = {0, 0, 0, 0, 0, 0, 0};

double Kp[7] = {2, 2, 2, 2, 2, 2, 2};
double Ki[7] = {0, 0, 0, 0, 0, 0, 0};
double Kd[7] = {1, 1, 1, 1, 1, 1, 1};

const char dirPin[7] = {0, 1, 2, 3, 4, 5, 6};
const char pwmPin[7] = {0, 1, 2, 3, 4, 5, 6};

const char spdLimit[7] = {255, 255, 255, 255, 255, 255, 255};
const bool reversed[7] = {0, 0, 0, 0, 0, 0, 0};

bool running = true;

const char enc_A[7] = {0, 1, 2, 3, 4, 5, 6};
const char enc_B[7] = {0, 1, 2, 3, 4, 5, 6};

void updatePID();
void drivers_initilize();
void update_velocity();
void update_encoders();
void update_goals();
void setup_interrupts();

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
#endif
