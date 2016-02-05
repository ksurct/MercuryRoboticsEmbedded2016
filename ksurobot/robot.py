# from .hardware.parts import RobotBase, LED, Motor
from .hardware.wiringpi_parts import (
    WPRobotBase as RobotBase,
    WPLED as LED,
    WPMotor as Motor
)
from .protocol.server import Server
from .protocol.proto.main_pb2 import Robot as RobotMsg
from .process_setup import process_setup


class Robot(RobotBase):
    def __init__(self):
        super().__init__()
        self.head_lights = self.attach_device(LED(6))
        self.motor_left = self.attach_device(Motor(20, 19, 18))
        self.motor_right = self.attach_device(Motor(17, 16, 13))


def main():
    process_setup()

    with Robot() as robot, Server(8002) as server:
        while True:
            msg = RobotMsg()
            msg.ParseFromString(server.recv())

            if msg.headlights.update:
                robot.head_lights.set(msg.headlights.on)
