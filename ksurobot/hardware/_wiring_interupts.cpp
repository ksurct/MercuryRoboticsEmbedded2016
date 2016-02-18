#include <wiringPi.h>
#include <sys/time.h>
#include <iostream>
#include <chrono>

using namespace std;


class SpeedPin {
public:
    SpeedPin(int *speed_output, int pin_a, int pin_b) {
        wiringPiISR(pin_a, INT_EDGE_BOTH, callback);
        pinMode(pin_a, INPUT);
        wiringPiISR(pin_b, INT_EDGE_BOTH, callback);
        pinMode(pin_b, INPUT);
        // last_tick =
        state = 0;
    }

private:
    long int last_tick;
    char state;

    void callback() {
        char new_state;
        bool forward;

        new_state = (digitalRead(pin_a) << 1) | digitalRead(pin_b);
        forward = (new_state == 0 && state == 3) || (new_state > state);
        state = new_state;
    }

    long int get_time() {
        return chrono::high_resolution_clock::now().time_since_epoch().count();
    }
}


/**
This creates a memory leak, but that's ok.
*/
extern "C"
void setup_speed_pin(int *speed_output, int pin_a, int pin_b) {
    new SpeedPin(speed_output, pin_a, pin_b);
}
