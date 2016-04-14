# from .hardware.parts import RobotBase, LED, Motor
from contextlib import suppress
import asyncio
import signal

from .hardware.wiringpi_parts import (
    WPRobotBase as RobotBase,
    WPLED as LED,
    WPMotor as Motor,
    CSpeedEncoder as SpeedEncoder
)

from .hardware.ir_sensor import IR_sensor
from .hardware.servo import Servo, HS5035Servo, TS53Servo, ContinuousServo, LaunchServo
from .protocol.server import Server as server_base
from .protocol.server2 import ClientlessWebSocketServer
from .process_setup import process_setup
from .controller import Controller
from .util import AsyncioLoop, get_config, PID
from .drivers import SpeedControlledMotor

MOTOR_PID = {
    'P': 0.1,
    'I': 0.0,
    'D': 0.02
}


class Robot(RobotBase):
    def __init__(self):
        super().__init__()

        self.head_lights = self.attach_device(LED(5))
        self.motor_left = self.attach_device(Motor(6, 13, 19, reverse=True))
        self.motor_left_speed = self.attach_device(SpeedEncoder(8, 25))
        self.motor_left_driver = SpeedControlledMotor(self.motor_left, self.motor_left_speed, PID.PID(**MOTOR_PID), reverse=True)
        self.motor_right = self.attach_device(Motor(24, 23, 18, reverse=True))
        self.motor_right_speed = self.attach_device(SpeedEncoder(17, 27))
        self.motor_right_driver = SpeedControlledMotor(self.motor_right, self.motor_right_speed, PID.PID(**MOTOR_PID), reverse=False)
        self.dist_fr = self.attach_device(IR_sensor(0))
        self.dist_fl= self.attach_device(IR_sensor(1))
        # self.camera = self.attach_device(Servo(0, 0))
        # self.launch = self.attach_device(Servo(0, 0))
        # self.claw  = self.attach_device(Servo(0, 0))

        self.camera = self.attach_device(HS5035Servo(1, 180))
        self.launch = self.attach_device(LaunchServo(2))
        self.claw  = self.attach_device(Servo(4, 0))
        self.wrist = self.attach_device(ContinuousServo(3))
        # self.dist_fr = self.attach_device(DistanceSensor(0))
        # self.dist_fl= self.attach_device(DistanceSensor(0))
        # self.dist_br = self.attach_device(DistanceSensor(0))
        # self.dist_bl = self.attach_device(DistanceSensor(0))


def main():
    config = get_config()
    process_setup()

    with Robot() as robot:
        server = ClientlessWebSocketServer(config.port)
        loop = asyncio.get_event_loop()
        controller = Controller(loop, robot, server)

        with AsyncioLoop() as loop:
            loop.submit(server.start_server())
            loop.submit(controller.run())
