from .hardware.parts import RobotBase, LED, Motor
from .protocol.server import Server


class Robot(RobotBase):
    def __init__(self):
        super().__init__()
        self.head_lights = self.attach_device(LED(17))
        self.motor_left = self.attach_device(Motor(20, 19, 18))
        self.motor_right = self.attach_device(Motor(17, 16, 13))


def main():

    with Robot() as robot, Server(8002) as server:
        while True:
            print(server.recv())
