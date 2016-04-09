from ctypes import cdll, c_int, CFUNCTYPE, POINTER, pointer, c_ubyte
from enum import Enum, IntEnum

from ..util import get_config

from .utils import Wrapper


libwiringpi = Wrapper('/usr/local/lib/libwiringPi.so.2.32')

wiringPiISR_cb = CFUNCTYPE(None)

wiringPiPiSPIDataRW_data = POINTER(c_ubyte)

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


@libwiringpi.wrap([c_int, c_int], c_int)
def wiringPiSPISetup (channel, speed):
    pass


@libwiringpi.wrap([c_int, wiringPiPiSPIDataRW_data, c_int], c_int)
def wiringPiSPIDataRW (channel, data, len):
    pass
