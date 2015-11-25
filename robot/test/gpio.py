"""
A shim that kinda-sorta emulates RPi.GPIO. Don't expect too much.

"""
import logging
logger = logging.getLogger(__name__)
logger.warning('using fake gpio')


class PWM(object):
    def __init__(self, pin, freq):
        pass

    def start(self, duty):
        pass

    def stop(self):
        pass

class GPIO_(object):
    BCM = 0
    OUT = 1
    PWM = PWM

    def __init__(self):
        self._setup = False
        self._setup_out_pins = set()

    def setmode(self, type):
        self._setup = True

    def setup(self, pin, type):
        if type is self.OUT:
            self._setup_out_pins.add(pin)
        else:
            raise NotImplemented

    def cleanup(self):
        self._setup = False


GPIO = GPIO_()
