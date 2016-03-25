#include <wiringPi.h>
#include <iostream>
#include <functional>
#include <mutex>

using namespace std;

class SpeedPin {
public:
    SpeedPin(long int *ticks, int pin_a, int pin_b) {
        function<void()> z = [=]() {this->callback();};
        auto func = z.target<void()>();

        wiringPiISR(pin_a, INT_EDGE_BOTH, func);
        pinMode(pin_a, INPUT);
        wiringPiISR(pin_b, INT_EDGE_BOTH, func);
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

    static void shim(SpeedPin* self) {
        self->callback();
    }

    void callback() {
        lock_guard<mutex> lock(this->lock);
        char new_state;
        bool forward;

        new_state = (digitalRead(pin_a) << 1) | digitalRead(pin_b);
        forward = (new_state == 0 && this->state == 3) || (new_state > this->state);

        forward ? this->ticks-- : this->ticks++;
        this->state = new_state;
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
