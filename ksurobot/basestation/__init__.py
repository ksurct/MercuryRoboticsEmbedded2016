from contextlib import suppress
from .controller import Controller
from ..protocol.proto.main_pb2 import Robot as RobotMessage, BaseStation
from ..util import get_config
import asyncio
import websockets
import logging
from sys import stdout

logger = logging.getLogger(__name__)


class Component(object):
    def __init__(self, **kwargs):
        self.parts = kwargs
        self.state = {k: None for k in kwargs}

    def check_updates(self, msg):
        needs_update = False
        for k, v in self.parts.items():
            new_value = v()
            old_value = self.state[k]
            if new_value != old_value:
                needs_update = True
                setattr(msg, k, new_value)
                msg.update = True

            self.state[k] = new_value
        return needs_update


class RobotState(object):
    def __init__(self, controller):
        self.controller = controller

        self.headlights = Component(on=controller.get_y)
        self.motor_right = Component(
            # speed=lambda: int(controller.get_left_y() * -120),
            speed=lambda: self.calculate_motor_speed()[0],
            breaks=controller.get_b)
        self.motor_left = Component(
            # speed=lambda: int(controller.get_left_y() * -120),
            speed=lambda: self.calculate_motor_speed()[1],
            breaks=controller.get_b)

    def _neg(self, num):
        if num < 0:
            return -1
        return 1

    def calculate_motor_speed(self):
        x = self.controller.get_left_x()
        y = self.controller.get_left_y()

        r, l = -y, -y
        # r_neg = self._neg()
        # l_neg = self._neg()

        # forward_value = abs(int((abs(y) - abs(x)) * 100))
        #
        # if abs(x) > abs(y) or y > 0:
        #     if x > 0:
        #         forward_value *= -1
        # #     100 + forward_value
        #
        # return int(x)

        # if x < 0:
        #     r += x
        # else:
        #     l -= x
        x *= 1
        r += -x/4
        l += x/4

        modifier = 120
        if self.controller.get_x():
            modifier = 60

        r = int(r*modifier)
        l = int(l*modifier)
        return r, l

async def run(url):
    logger.info('Connecting to {}'.format(url))

    Controller.init()
    controller = Controller(0)

    robot_state = RobotState(controller)

    async with websockets.connect(url) as websocket:
        headlights_state = False
        headlights_btn_state = False

        while True:
            controller.update()

            robot_msg = RobotMessage()

            # robot_msg.motor_left_rpm.update = True
            # robot_msg.motor_left_rpm.speed = 120
            #
            # robot_msg.motor_right_rpm.update = True
            # robot_msg.motor_right_rpm.speed = 120
            # robot_msg.arm.update = True
            # robot_msg.arm.degree = 10
            # robot_msg.wrist.update = True
            # robot_msg.wrist.degree = 2
            # robot_msg.camera.update = True
            # robot_msg.camera.degree = 0
            robot_msg.claw.update = True
            robot_msg.claw.degree = controller.get_a() * 90

            robot_msg.arm.update = True
            if controller.get_right_trigger() > 0.9:
                robot_msg.arm.degree = 5304
            else:
                robot_msg.arm.degree = 3120

            robot_msg.camera.update = True
            robot_msg.camera.degree = 190 - int((controller.get_right_x()) * 190)

            if headlights_btn_state ^ controller.get_y():
                headlights_btn_state = controller.get_y()
                if headlights_btn_state == True:
                    headlights_state = not headlights_state
                    robot_msg.headlights.update = True
                    robot_msg.headlights.on = headlights_state
            # robot_state.headlights.check_updates(robot_msg.headlights)
            robot_state.motor_right.check_updates(robot_msg.motor_right_rpm)
            robot_state.motor_left.check_updates(robot_msg.motor_left_rpm)

            ser_msg = robot_msg.SerializeToString()

            await websocket.send(ser_msg)

            with suppress(asyncio.TimeoutError):
                msg = await asyncio.wait_for(websocket.recv(), .1)
                # print(msg)
                base_msg = BaseStation()
                base_msg.ParseFromString(msg)

                print("SD left ", base_msg.sensor_data.front_left)
                print("SD right ", base_msg.sensor_data.front_right)

def main():
    config = get_config()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run("ws://{0.addr}:{0.port}".format(config)))
