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
    pass


class WPMotor(object):
    pass
