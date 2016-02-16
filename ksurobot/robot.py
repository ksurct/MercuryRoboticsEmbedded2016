# from .hardware.parts import RobotBase, LED, Motor
from .hardware.wiringpi_parts import (
    WPRobotBase as RobotBase,
    WPLED as LED,
    WPMotor as Motor,
    WPSpeedEncoder as SpeedEncoder
)
from .protocol.server import Server as server_base
from .protocol.proto.main_pb2 import Robot as RobotMsg
from .process_setup import process_setup


class Robot(RobotBase):
    def __init__(self):
        super().__init__()
        self.head_lights = self.attach_device(LED(6))
        self.motor_left = self.attach_device(Motor(20, 19, 18))
        self.motor_left_speed = self.attach_device(SpeedEncoder(22, 21))
        self.motor_right = self.attach_device(Motor(17, 16, 13))
        self.motor_right_speed = self.attach_device(SpeedEncoder(24, 23))


Server = lambda: server_base(8002)


def main():
    process_setup()

    with Robot() as robot, Server() as server:
        while True:
            msg = RobotMsg()
            msg.ParseFromString(server.recv())

            if msg.headlights.update:
                robot.head_lights.set(msg.headlights.on)
