#include <wiringPi.h>
#include <iostream>
#include <functional>
#include <mutex>

using namespace std;

class SpeedPin {
public:
    SpeedPin(long int *ticks, int pin_a, int pin_b) {
        wiringPiDataISR(pin_a, INT_EDGE_BOTH, (void (*)(void*)) &SpeedPin::callback, this);
        pinMode(pin_a, INPUT);
        wiringPiDataISR(pin_b, INT_EDGE_BOTH, (void (*)(void*)) &SpeedPin::callback, this);
        pinMode(pin_b, INPUT);
        this->ticks = ticks;
        this->pin_a = pin_a;
        this->pin_b = pin_b;
    }

private:
    mutex lock;
    long int *ticks;
    char state;
    int pin_a;
    int pin_b;

    static void callback(SpeedPin* self) {
        lock_guard<mutex> lock(self->lock);
        const int states [] = {1, 3, 0, 2};
        char new_state;
        bool forward;

        new_state = (digitalRead(self->pin_a) << 1) | digitalRead(self->pin_b);
        forward = (new_state == 0 && self->state == 3) || (new_state > self->state);

        forward = states[new_state] == self->state;
        forward ? (*self->ticks)-- : (*self->ticks)++;
        self->state = new_state;
    }
};


/**
This creates a memory leak, but that's ok.
*/
extern "C" {
    void setup_speed_pin(long int *last_tick, int pin_a, int pin_b) {
        new SpeedPin(last_tick, pin_a, pin_b);
    }
}
