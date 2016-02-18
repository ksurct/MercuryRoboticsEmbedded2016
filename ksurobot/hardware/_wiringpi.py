from ctypes import cdll, c_int, CFUNCTYPE, pointer
from enum import Enum, IntEnum

libwiringpi = cdll.LoadLibrary('libwiringPi.so.2.31')


wiringPiISR_cb = CFUNCTYPE(None)


def _wrap(args, result):
    def _w(func):
        func = getattr(libwiringpi, func.__name__)
        func.argtypes = args
        func.restype = result
        return func
    return _w


class PinModes(IntEnum):
    INPUT = 0
    OUTPUT = 1
    PWM_OUTPUT = 2
    GPIO_CLOCK = 3
    SOFT_PWM_OUTPUT = 4
    SOFT_TONE_OUTPUT = 5
    PWM_TONE_OUTPUT = 6


class PullModes(IntEnum):
    PUD_OFF = 0
    PUD_DOWN = 1
    PUD_UP = 2


class InterruptModes(IntEnum):
    INT_EDGE_SETUP = 0
    INT_EDGE_FALLING = 1
    INT_EDGE_RISING = 2
    INT_EDGE_BOTH = 3


@_wrap([], None)
def wiringPiSetup():
    pass


@_wrap([], None)
def wiringPiSetupSys():
    pass


@_wrap([], None)
def wiringPiSetupGpio():
    pass


@_wrap([], None)
def wiringPiSetupPhys():
    pass


@_wrap([c_int, c_int], None)
def pinModeAlt(pin, mode):
    pass


@_wrap([c_int], None)
def pwmSetClock(speed):
    pass


@_wrap([c_int, c_int], None)
def pinMode(pin, mode):
    pass


@_wrap([c_int, c_int], None)
def pullUpDnControl(pin, pud):
    pass


@_wrap([c_int], c_int)
def digitalRead(pin):
    pass


@_wrap([c_int, c_int], None)
def digitalWrite(pin, value):
    pass


@_wrap([c_int, c_int], None)
def pwmWrite(pin, value):
    pass


@_wrap([c_int, c_int, wiringPiISR_cb], None)
def wiringPiISR(pin, mode, callback):
    pass


# Extentions
interupts_library = cdll.LoadLibrary('./_wiring_interupts.so')


def _wrap(args, result):
    def _w(func):
        func = getattr(interupts_library, func.__name__)
        func.argtypes = args
        func.restype = result
        return func
    return _w


@_wrap([pointer(c_int), c_int, c_int], None)
def setup_speed_pin(int *speed_output, int pin_a, int pin_b):
    pass
