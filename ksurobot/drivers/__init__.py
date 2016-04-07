"""
High level interfaces and control structures for
hardware and software.
"""
from ..hardware.wiringpi_parts import WPMotor, WPSpeedEncoder
from ..util.PID import PID


class SpeedControlledMotor(object):
    def __init__(self, motor, encoder, pid):
        assert isinstance(motor, WPMotor)
        assert isinstance(encoder, WPSpeedEncoder)
        assert isinstance(pid, PID)
        self.motor = motor
        self.encoder = encoder
        self.pid = pid

        self._brake = True

    def tick(self):
        if self._brake is True:
            self.motor.set_brake(0)
            self._brake = None
        elif self._brake is None:
            pass
        else:
            self.pid.update(self.encoder.get())
            self.motor.set(self.pid.output)

    def set(self, rpm):
        self._brake = False
        self.pid.SetPoint(rpm)

    def set_brake(self):
        self._brake = True
