from contextlib import ExitStack
# import _wiringpi2

from . import _wiringpi as wiringpi2
from ctypes import CFUNCTYPE

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
    def __init__(self, dir_pin_a, dir_pin_b, speed_pin):
        self.dir_pin_a = dir_pin_a
        self.dir_pin_b = dir_pin_b
        self.speed_pin = speed_pin

    def __enter__(self):
        wiringpi2.pinMode(self.dir_pin_a, wiringpi2.PinModes.OUTPUT)
        wiringpi2.pinMode(self.dir_pin_b, wiringpi2.PinModes.OUTPUT)
        wiringpi2.pinMode(self.speed_pin, wiringpi2.PinModes.PWM_OUTPUT)
        self.set_feq(10000)
        self.set(0)

    def __exit__(self, *enc):
        pass

    def set(self, speed):
        speed = speed*1024//100
        if speed < 0:
            wiringpi2.digitalWrite(self.dir_pin_a, 0)
            wiringpi2.digitalWrite(self.dir_pin_b, 1)
            speed = -speed
        else:
            wiringpi2.digitalWrite(self.dir_pin_a, 1)
            wiringpi2.digitalWrite(self.dir_pin_b, 0)
        wiringpi2.pwmWrite(self.speed_pin, speed)

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


class WPSpeedEncoder(object):
    def __init__(self, pin_a, pin_b):
        self.pin_a = pin_a
        self.pin_b = pin_b

    def __enter__(self):
        wiringpi2.wiringPiISR(self.pin_a, wiringpi2.InterruptModes.INT_EDGE_FALLING, self.callback_a)
        wiringpi2.wiringPiISR(self.pin_b, wiringpi2.InterruptModes.INT_EDGE_FALLING, self.callback_b)

    def __exit__(self, *enc):
        pass

    @wiringpi2.wiringPiISR_cb
    def callback_a():
        print('callback_a')

    @wiringpi2.wiringPiISR_cb
    def callback_b():
        print('callback_b')
