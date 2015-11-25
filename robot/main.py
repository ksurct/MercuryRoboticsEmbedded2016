from .hardware.parts import RobotBase, LED, Motor
from .protocol.server import Server


def main():
    class Robot(RobotBase):
        def __init__(self):
            super().__init__()
            self.head_lights = self.attach_device(LED(17))
            self.motor_left = self.attach_device(Motor(23, 24, 25))
            self.motor_right = self.attach_device(Motor(26, 27, 28))

    with Robot() as robot, Server(8002) as server:

        print(server.recv())
