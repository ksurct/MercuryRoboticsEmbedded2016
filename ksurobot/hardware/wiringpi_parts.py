from contextlib import ExitStack
# import _wiringpi2

from ._wiringpi import c_libs as wiringpi2


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
        wiringpi2.pinMode(self.pin, wiringpi2.GPIO.OUTPUT)
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
        wiringpi2.pinMode(self.dir_pin_a, wiringpi2.GPIO.OUTPUT)
        wiringpi2.pinMode(self.dir_pin_b, wiringpi2.GPIO.OUTPUT)
        wiringpi2.pinMode(self.speed_pin, wiringpi2.GPIO.PWM_OUTPUT)
        wiringpi2.pwmSetClock(10000)
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


class WPSpeedEncoder(object):
    def __init__(self, pin_a, pin_b):
        self.pin_a = pin_a
        self.pin_b = pin_b

    def __enter__(self):
        pass
        # wiringpi2.wiringPiISR(self.pin_a, wiringpi2.GPIO.INT_EDGE_FALLING, self.callback_a)
        # wiringpi2.wiringPiISR(self.pin_a, wiringpi2.GPIO.INT_EDGE_FALLING, self.callback_b)

    def __exit__(self, *enc):
        pass

    def callback_a(self):
        print('callback_a')

    def callback_b(self):
        print('callback_b')
