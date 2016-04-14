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
        msg.sensor_data.front_left = int(self.robot.dist_fl.get())
        msg.sensor_data.front_right = int(self.robot.dist_fr.get())
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

        if msg.arm.update:
            self.robot.launch.setTarget(msg.arm.degree)

        if msg.claw.update:
            self.robot.claw.setAngle(msg.claw.degree)

        if msg.camera.update:
            self.robot.camera.setAngle(msg.camera.degree)

        if msg.wrist.update:
            if msg.wrist.degree == 1:
                self.robot.wrist.moveLeft()
            if msg.wrist.degree == 2:
                self.robot.wrist.nudgeLeft()
            if msg.wrist.degree == 3:
                self.robot.wrist.nudgeRight()
            if msg.wrist.degree == 4:
                self.robot.wrist.moveRight()

        for motor_str in ('right', 'left'):
            motor = getattr(self.robot, 'motor_'+motor_str)
            msg_motor = getattr(msg, 'motor_'+motor_str)
            if msg_motor.update:
                if msg_motor.breaks:
                    motor.set_brake(True)
                else:
                    motor.set(msg_motor.speed)
            # Per rpm code
            motor = getattr(self.robot, 'motor_'+motor_str+'_driver')
            msg_motor = getattr(msg, 'motor_'+motor_str+'_rpm')
            if msg_motor.update:
                if msg_motor.breaks:
                    motor.set_brake(True)
                else:
                    motor.set(msg_motor.speed)

    async def _wait_sample(self):
        while True:
            await asyncio.sleep(.025)
            self.robot.motor_left_speed.update()
            self.robot.motor_right_speed.update()
            self.robot.motor_left_driver.update()
            self.robot.motor_right_driver.update()

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

    async def _wait_sensorread(self):
        logger.info('Start sensorread loop')
        while True:
            await asyncio.sleep(.03)
            self.robot.dist_fr.update()
            self.robot.dist_fl.update()


    async def _wait_throw(self):
        while True:
            await asyncio.sleep(.2)
            await self.event_throwing.wait()
            self.throw_tick()


    async def run(self):
        logger.info('Start main loop')
        asyncio.ensure_future(self._wait_recv())
        asyncio.ensure_future(self._wait_heartbeat())

        asyncio.ensure_future(self._wait_sensorread())

        asyncio.ensure_future(self._wait_sample())
