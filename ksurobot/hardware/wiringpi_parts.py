from contextlib import ExitStack
import wiringpi2


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
        wiringpi2.pinMode(self.pin, 1)

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

        self.speed_pwm = None

    def __enter__(self):
        pass
        # GPIO.setup(self.dir_pin_a, GPIO.OUT)
        # GPIO.setup(self.dir_pin_b, GPIO.OUT)
        # GPIO.setup(self.speed_pin, GPIO.OUT)
        # self.speed_pwm = GPIO.PWM(self.speed_pin, 5000)
        # self.speed_pwm.start(0)

    def __exit__(self, *enc):
        pass
        # self.speed_pwm.stop()
        # self.speed_pwm = None

    def set(self, speed):
        pass
        # if speed < 0:
        #     GPIO.output(self.dir_pin_a, False)
        #     GPIO.output(self.dir_pin_b, True)
        #     speed = -speed
        # else:
        #     GPIO.output(self.dir_pin_a, True)
        #     GPIO.output(self.dir_pin_b, False)
        # self.speed_pwm.ChangeDutyCycle(speed)

    def set_feq(self, feq):
        pass
        # self.speed_pwm.ChangeFrequency(feq)

    def set_brake(self, type):
        pass
        # if type == 0:
        #     GPIO.output(self.dir_pin_a, False)
        #     GPIO.output(self.dir_pin_b, False)
        # else:  # Maybe better
        #     GPIO.output(self.dir_pin_a, True)
        #     GPIO.output(self.dir_pin_b, True)

    def get(self):
        return 0
