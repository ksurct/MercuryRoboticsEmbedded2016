from ctypes import cdll, c_int, CFUNCTYPE
from enum import Enum, IntEnum

from ..util import get_config


class Wrapper(object):
    def __init__(self, library):
        self.library_name = library
        self.library = None

    def load(self):
        if self.library is None:
            config = get_config()
            if config.emulate:
                self.library = False
            else:
                self.library = cdll.LoadLibrary(self.library_name)

        return self.library

    def wrap(self, args, result):
        lib = self.load()
        def _w(func):
            if lib:
                func = getattr(lib, func.__name__)
                func.argtypes = args
                func.restype = result
            return func
        return _w


libwiringpi = Wrapper('libwiringPi.so.2.31')

wiringPiISR_cb = CFUNCTYPE(None)


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


@libwiringpi.wrap([], None)
def wiringPiSetup():
    pass


@libwiringpi.wrap([], None)
def wiringPiSetupSys():
    pass


@libwiringpi.wrap([], None)
def wiringPiSetupGpio():
    pass


@libwiringpi.wrap([], None)
def wiringPiSetupPhys():
    pass


@libwiringpi.wrap([c_int, c_int], None)
def pinModeAlt(pin, mode):
    pass


@libwiringpi.wrap([c_int], None)
def pwmSetClock(speed):
    pass


@libwiringpi.wrap([c_int, c_int], None)
def pinMode(pin, mode):
    pass


@libwiringpi.wrap([c_int, c_int], None)
def pullUpDnControl(pin, pud):
    pass


@libwiringpi.wrap([c_int], c_int)
def digitalRead(pin):
    pass


@libwiringpi.wrap([c_int, c_int], None)
def digitalWrite(pin, value):
    pass


@libwiringpi.wrap([c_int, c_int], None)
def pwmWrite(pin, value):
    pass


@libwiringpi.wrap([c_int, c_int, wiringPiISR_cb], None)
def wiringPiISR(pin, mode, callback):
    pass
