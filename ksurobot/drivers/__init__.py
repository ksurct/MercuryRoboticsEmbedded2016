"""
High level interfaces and control structures for
hardware and software.
"""
from ..hardware.wiringpi_parts import WPMotor, WPSpeedEncoder
from ..util.PID import PID

def limit100(num):
    return max(-100, min(100, num))


class SpeedControlledMotor(object):
    def __init__(self, motor, encoder, pid, reverse=False, squelch=5):
        assert isinstance(motor, WPMotor)
        assert isinstance(pid, PID)
        self.motor = motor
        self.encoder = encoder
        self.pid = pid

        self._brake = True
        self._power = 0
        self._reverse = reverse
        self._squelch = squelch

    def update(self):
        if self._brake is True:
            self._power = 0
            self.set(0)
            self.motor.set_brake(0)
        else:
            self.pid.update(self.encoder.get())
            self._power -= self.pid.output
            self._power = limit100(self._power)
            pwr = self._power
            if abs(pwr) < self._squelch:
                pwr = 0
            self.motor.set(pwr)

    def get_output(self):
        return self._power

    def set(self, rpm):
        self._brake = False
        if self._reverse:
            rpm = -rpm
        self.pid.SetPoint = rpm

    def set_brake(self, type):
        self._brake = True
