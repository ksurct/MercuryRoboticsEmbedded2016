from contextlib import ExitStack
from threading import Lock
# import _wiringpi2

from . import _wiringpi as wiringpi2
from ._wiringpi_encoders import setup_speed_pin
from ctypes import CFUNCTYPE, pointer, c_byte, c_long

from .bases_encoders import BaseEncoder


class WPRobotBase(object):
    def __init__(self):
        self.context = None
        self.devices = []

    def __enter__(self):
        wiringpi2.wiringPiSetupGpio()
        self.context = ExitStack()
        for device in self.devices:
            self.context.enter_context(device)
        return self

    def __exit__(self, *exc):
        self.context.__exit__(*exc)

    def attach_device(self, device):
        self.devices.append(device)
        return device


class WPLED(object):
    def __init__(self, num):
        self.pin = num

    def __enter__(self):
        wiringpi2.pinMode(self.pin, wiringpi2.PinModes.OUTPUT)
        self.set(False)

    def __exit__(self, *enc):
        pass

    def set(self, state):
        wiringpi2.digitalWrite(self.pin, int(state))

    def get(self):
        return bool(wiringpi2.digitalRead(self.pin))


class WPMotor(object):
    def __init__(self, dir_pin_a, dir_pin_b, speed_pin, reverse=False):
        self.dir_pin_a = dir_pin_a
        self.dir_pin_b = dir_pin_b
        self.speed_pin = speed_pin
        self.reverse = reverse

    def __enter__(self):
        wiringpi2.pinMode(self.dir_pin_a, wiringpi2.PinModes.OUTPUT)
        wiringpi2.pinMode(self.dir_pin_b, wiringpi2.PinModes.OUTPUT)
        wiringpi2.pinMode(self.speed_pin, wiringpi2.PinModes.PWM_OUTPUT)
        self.set_feq(10000)
        self.set(0)

    def __exit__(self, *enc):
        self.set(0)

    def set(self, speed):
        if self.reverse:
            speed = -speed
        speed = speed*1024//100
        if speed < 0:
            wiringpi2.digitalWrite(self.dir_pin_a, 0)
            wiringpi2.digitalWrite(self.dir_pin_b, 1)
            speed = -speed
        else:
            wiringpi2.digitalWrite(self.dir_pin_a, 1)
            wiringpi2.digitalWrite(self.dir_pin_b, 0)
        wiringpi2.pwmWrite(self.speed_pin, int(speed))

    def set_feq(self, feq):
        wiringpi2.pwmSetClock(feq)

    def set_brake(self, type):
        if type == 0:
            wiringpi2.digitalWrite(self.dir_pin_a, 0)
            wiringpi2.digitalWrite(self.dir_pin_b, 0)
        else:  # Maybe better
            wiringpi2.digitalWrite(self.dir_pin_a, 1)
            wiringpi2.digitalWrite(self.dir_pin_b, 1)

    def get(self):
        return 0


class WPSpeedEncoder(BaseEncoder):
    def __init__(self, pin_a, pin_b):
        super().__init__()
        self.pin_a = pin_a
        self.pin_b = pin_b

        self.ticks = 0
        self.state = 0
        self.lock = Lock()
        self._gc_roots = []

    def __enter__(self):
        cb = wiringpi2.wiringPiISR_cb(lambda: self.callback())
        self._gc_roots.append(cb)
        wiringpi2.pinMode(self.pin_a, wiringpi2.PinModes.INPUT)
        wiringpi2.wiringPiISR(self.pin_a, wiringpi2.InterruptModes.INT_EDGE_FALLING, cb)
        wiringpi2.pinMode(self.pin_b, wiringpi2.PinModes.INPUT)
        wiringpi2.wiringPiISR(self.pin_b, wiringpi2.InterruptModes.INT_EDGE_FALLING, cb)

    def get_ticks(self):
        with self.lock:
            return self.ticks

    def callback(self):
        FORWARD = [1, 3, 0, 2]
        with self.lock:
            a = wiringpi2.digitalRead(self.pin_a)
            b = wiringpi2.digitalRead(self.pin_b)
            new_state = (a << 1) | b

            forward = FORWARD[new_state] == self.state
            if forward:
                self.ticks += 1
            else:
                self.ticks -= 1
            self.state = new_state


class CSpeedEncoder(BaseEncoder):
    def __init__(self, pin_a, pin_b, **kwargs):
        super().__init__(**kwargs)
        self.pin_a = pin_a
        self.pin_b = pin_b

        self.ticks = c_long()

    def __enter__(self):
        setup_speed_pin(pointer(self.ticks), self.pin_a, self.pin_b)
        return self

    def get_ticks(self):
        return self.ticks.value
