import asyncio
import logging
from contextlib import suppress
from .protocol.proto.main_pb2 import Robot as RobotMsg, BaseStation as BaseStationMsg

logger = logging.getLogger(__name__)


class Controller(object):
    def __init__(self, loop, robot, server):
        self.robot = robot
        self.server = server
        self.loop = loop
        self.event_throwing = asyncio.Event()
        self.event_throwing.clear()

    def heartbeat(self):
        msg = BaseStationMsg()
        msg.sensor_data.update = True
        msg.sensor_data.front_left = 3
        msg.sensor_data.front_right = 4
        msg.sensor_data.back_left = 5
        msg.sensor_data.back_right = 6
        return msg.SerializeToString()

    def throw_tick(self):
        pass

    def recv(self, msg_):
        logger.debug('Recv msg {}'.format(msg_))
        msg = RobotMsg()
        msg.ParseFromString(msg_)

        for proc in msg.procedures:
            proc_name = proc.WhichOneof('procedure')
            if proc_name == 'throw':
                self.event_throwing.set()
            elif proc_name == 'abort':
                self.event_throwing.clear()

        if self.event_throwing.is_set():
            return

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
            # Per rpm code
            motor = getattr(self.robot, 'motor_'+motor_str+'_speed')
            msg_motor = getattr(msg, 'motor_'+motor_str+'_rpm')
            if msg_motor.update:
                if msg_motor.breaks:
                    motor.set_brake(True)
                else:
                    motor.set(msg_motor.speed)



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

    async def _wait_throw(self):
        while True:
            await asyncio.sleep(.2)
            await self.event_throwing.wait()
            self.throw_tick()

    async def run(self):
        logger.info('Start main loop')
        asyncio.ensure_future(self._wait_recv())
        asyncio.ensure_future(self._wait_heartbeat())
