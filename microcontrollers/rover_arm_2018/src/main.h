#ifndef main_h
#define main_h

int goal_pos[7] = {0, 0, 0, 0, 0, 0, 0};            // position vector
volatile int actual_pos[7] = {0, 0, 0, 0, 0, 0, 0}; // actual position vector
int vel[7] = {0, 0, 0, 0, 0, 0, 0};

double Kp[7] = {2, 2, 2, 2, 2, 2, 2};
double Ki[7] = {0, 0, 0, 0, 0, 0, 0};
double Kd[7] = {1, 1, 1, 1, 1, 1, 1};

const char dirPin[7] = {0, 1, 2, 3, 4, 5, 6};
const char pwmPin[7] = {0, 1, 2, 3, 4, 5, 6};

const char spdLimit[7] = {255, 255, 255, 255, 255, 255, 255};
const bool reversed[7] = {0, 0, 0, 0, 0, 0, 0};

//const char low_pos_limit = {0, 0, 0, 0, 0, 0, 0};
//const char high_pos_limit = {0, 0, 0, 0, 0, 0, 0};

bool running = true;

const char enc_A[7] = {0, 1, 2, 3, 4, 5, 6};
const char enc_B[7] = {0, 1, 2, 3, 4, 5, 6};

void updatePID();
void drivers_initilize();
void update_velocity();
void update_encoders();
void update_goals();
void setup_interrupts();

#endif
