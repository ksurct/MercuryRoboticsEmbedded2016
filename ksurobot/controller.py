import asyncio
import logging
from contextlib import suppress
from enum import Enum
from .protocol.proto.main_pb2 import Robot as RobotMsg, BaseStation as BaseStationMsg

logger = logging.getLogger(__name__)

AUTOSTOP = 6

class BlockedEnum:
    FRONT = 0
    BACK = 1


class Controller(object):
    def __init__(self, loop, robot, server):
        self.robot = robot
        self.server = server
        self.loop = loop
        self.blocked = {}

    def heartbeat(self):
        msg = BaseStationMsg()
        msg.sensor_data.update = True
        msg.sensor_data.front_left = 3
        msg.sensor_data.front_right = 4
        msg.sensor_data.back_left = 5
        msg.sensor_data.back_right = 6
        return msg.SerializeToString()

    def recv(self, msg_):
        logger.debug('Recv msg {}'.format(msg_))
        msg = RobotMsg()
        msg.ParseFromString(msg_)

        if msg.headlights.update:
            self.robot.head_lights.set(msg.headlights.on)

        for motor_str in ('right', 'left'):
            motor = getattr(self.robot, 'motor_'+motor_str)
            msg_motor = getattr(msg, 'motor_'+motor_str)
            if msg_motor.update:
                if msg_motor.breaks:
                    motor.set_brake(True)
                else:
                    motor.set(msg_motor.speed)

    def auto_stop(self):
        avg_front = (self.robot.dist_fl.get_clean() + self.robot.dist_fr.get_clean()) / 2
        avg_speed = (self.robot.motor_right.get() + self.motor_right.get())
        if avg_front < AUTOSTOP:
            self.auto_stop.add(BlockedEnum.FRONT)
            self.robot.motor_right.set_brake()
            self.robot.motor_left.set_brake()
        # self.robot.dist_bl.get_clean()

    def _do_update_motor(self, rate):
        if rate > 0 and BlockedEnum.FRONT not in self.blocked:
            return False
        else:
            return True

    async def _wait_recv(self):
        logger.info('Start recv loop')
        while True:
            msg = await self.server.recv()
            self.recv(msg)

    async def _wait_heartbeat(self):
        logger.info('Start heartbeat loop')
        while True:
            await asyncio.sleep(.3)
            msg = self.heartbeat()
            await self.server.send(msg)

    async def _wait_auto_stop(self):
        logger.info('Start auto stop loop')
        while True:
            await asyncio.sleep(.5)
            self.auto_stop()

    async def run(self):
        logger.info('Start main loop')
        asyncio.ensure_future(self._wait_recv())
        asyncio.ensure_future(self._wait_heartbeat())
