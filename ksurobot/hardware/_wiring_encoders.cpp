#include <wiringPi.h>
#include <iostream>
#include <functional>
#include <mutex>

using namespace std;



class SpeedPin {
public:
    SpeedPin(int num, long int *ticks, int pin_a, int pin_b) {
        speed_pins[num] = this;
        if (num == 0) {
            wiringPiISR(pin_a, INT_EDGE_BOTH, callback_1);
            wiringPiISR(pin_b, INT_EDGE_BOTH, callback_1);
        }
        else if (num == 1) {
            wiringPiISR(pin_a, INT_EDGE_BOTH, callback_2);
            wiringPiISR(pin_b, INT_EDGE_BOTH, callback_2);
        }

        pinMode(pin_a, INPUT);
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

    static SpeedPin* speed_pins[2];
    static void callback_1() {
        speed_pins[0]->callback();
    }
    static void callback_2() {
        speed_pins[1]->callback();
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
    void setup_speed_pin(int num, long int *last_tick, int pin_a, int pin_b) {
        new SpeedPin(num, last_tick, pin_a, pin_b);
    }
}
