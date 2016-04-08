from contextlib import ExitStack
from logging import getLogger

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    from ..test.gpio import GPIO

logger = getLogger(__name__)


class LED(object):
    def __init__(self, num):
        self.pin = num

    def __enter__(self):
        GPIO.setup(self.pin, GPIO.OUT)

    def __exit__(self, *enc):
        pass

    def set(self, state):
        GPIO.output(self.pin, state)

    def get(self):
        return bool(GPIO.input(self.pin))


class Motor(object):
    def __init__(self, dir_pin_a, dir_pin_b, speed_pin):
        self.dir_pin_a = dir_pin_a
        self.dir_pin_b = dir_pin_b
        self.speed_pin = speed_pin

        self.speed_pwm = None

    def __enter__(self):
        GPIO.setup(self.dir_pin_a, GPIO.OUT)
        GPIO.setup(self.dir_pin_b, GPIO.OUT)
        GPIO.setup(self.speed_pin, GPIO.OUT)
        self.speed_pwm = GPIO.PWM(self.speed_pin, 5000)
        self.speed_pwm.start(0)

    def __exit__(self, *enc):
        self.speed_pwm.stop()
        self.speed_pwm = None

    def set(self, speed):
        if speed < 0:
            GPIO.output(self.dir_pin_a, False)
            GPIO.output(self.dir_pin_b, True)
            speed = -speed
        else:
            GPIO.output(self.dir_pin_a, True)
            GPIO.output(self.dir_pin_b, False)
        self.speed_pwm.ChangeDutyCycle(speed)

    def set_feq(self, feq):
        self.speed_pwm.ChangeFrequency(feq)

    def set_brake(self, type):
        if type == 0:
            GPIO.output(self.dir_pin_a, False)
            GPIO.output(self.dir_pin_b, False)
        else:  # Maybe better
            GPIO.output(self.dir_pin_a, True)
            GPIO.output(self.dir_pin_b, True)

    def get(self):
        return 0


class RobotBase(object):
    def __init__(self):
        self.context = None
        self.devices = []

    def __enter__(self):
        GPIO.setmode(GPIO.BCM)
        self.context = ExitStack()
        for device in self.devices:
            self.context.enter_context(device)
        return self

    def __exit__(self, *exc):
        self.context.__exit__(*exc)
        GPIO.cleanup()

    def attach_device(self, device):
        self.devices.append(device)
        return device
