from time import sleep

from ._maestro import Controller

control = Controller()


class Servo(object):

    def __init__(self, my_id, initPos = 0, x = 3990):
        """
        my_id = the ID of the servo
        initPos = The initial position to place servo at in degrees, defaults to 0
        x = the "0" position of the servo in quarter-microseconds
        """
        self.my_id = my_id
        self.controller = control
        self.x = x
        self.y = 7910
        self.controller.setRange(self.my_id, 4000, 8000)
        self.controller.setSpeed(self.my_id, 0)
        self.controller.setAccel(self.my_id, 0)
        self.setAngle(initPos)

    def __enter__(self):
        return self

    def __exit__(self, *enc):
        pass

    def setAngle(self, degrees):
        self.controller.setTarget(self.my_id, self.conv(degrees))

    def setTarget(self, target):
        self.controller.setTarget(self.my_id, target)

    def getPos(self):
        return self.controller.getPosition(self.my_id)

    def isMoving(self):
        return self.controller.isMoving(self.my_id)

    def getMyID(self):
        return self.my_id

    def conv(self, degrees):
        return int(self.x + degrees * ((self.y - self.x)/(90)))

class TitaniumServo(Servo):
    x = 4000
    y = 8000

    def __init__(self, my_id, initPos = 0):
        """
        my_id = the ID of the servo
        initPos = The initial position to place servo at in degrees, defaults to 0
        """
        self.my_id = my_id
        self.controller = control
        self.controller.setRange(self.my_id, 0, 0)
        self.controller.setSpeed(self.my_id, 0)
        self.controller.setAccel(self.my_id, 0)
        self.controller.setRange(self.my_id, self.x, self.y)
        self.setAngle(initPos)

    def setAngle(self, degrees):
        self.controller.setTarget(self.my_id, self.conv(degrees))

    def conv(self, degrees):
        return int(self.x + 42 * degrees)

class System3000Servo(Servo):
    x = 4000
    y = 8000

    def __init__(self, my_id, initPos = 0):
        """
        my_id = the ID of the servo
        rotation = the max rotation angle that the servo can go to
        initPos = The initial position to place servo at in degrees, defaults to 0
        """
        self.my_id = my_id
        self.controller = control
        self.controller.setRange(self.my_id, 0, 0)
        self.controller.setSpeed(self.my_id, 0)
        self.controller.setAccel(self.my_id, 0)
        self.controller.setRange(self.my_id, self.x, self.y)
        self.setAngle(initPos)

        def setAngle(self, degrees):
            self.controller.setTarget(self.my_id, self.conv(degrees))

        def conv(self, degrees):
            return int(self.x + 42 * degrees)

class HS5035Servo(Servo):
    x = 4380
    y = 7620

    def __init__(self, my_id, initPos = 0):
        """
        my_id = the ID of the servo
        rotation = the max rotation angle that the servo can go to
        initPos = The initial position to place servo at in degrees, defaults to 0
        """
        self.my_id = my_id
        self.controller = control
        self.controller.setRange(self.my_id, 0, 0)
        self.controller.setSpeed(self.my_id, 0)
        self.controller.setAccel(self.my_id, 0)
        self.controller.setRange(self.my_id, self.x, self.y)
        self.setAngle(initPos)

    def setAngle(self, degrees):
        self.controller.setTarget(self.my_id, self.conv(degrees))

    def conv(self, degrees):
        return int(self.x + 18 * degrees)


class TS53Servo(Servo):
    x = 1088
    y = 9152

    def __init__(self, my_id, initPos = 0):
        """
        my_id = the ID of the servo
        rotation = the max rotation angle that the servo can go to
        initPos = The initial position to place servo at in degrees, defaults to 0
        """
        self.my_id = my_id
        self.controller = control
        self.controller.setRange(self.my_id, 0, 0)
        self.controller.setSpeed(self.my_id, 0)
        self.controller.setAccel(self.my_id, 0)
        self.controller.setRange(self.my_id, self.x, self.y)
        self.setAngle(initPos)

    def setAngle(self, degrees):
        self.controller.setTarget(self.my_id, self.conv(degrees))

    def conv(self, degrees):
        return int(self.x + 45 * degrees)


class ContinuousServo(Servo):
    centerpoint = 5456

    def __init__(self, my_id):
        """
        my_id = the ID of the servo
        rotation = the max rotation angle that the servo can go to
        initPos = The initial position to place servo at in degrees, defaults to 0
        """
        self.my_id = my_id
        self.controller = control
        self.controller.setRange(self.my_id, 0, 0)
        self.controller.setSpeed(self.my_id, 0)
        self.controller.setAccel(self.my_id, 0)
        self.controller.setRange(self.my_id, 4000, 8000)
        self.setAngle(self.centerpoint)

    def nudgeLeft(self):
        self.setAngle(self.centerpoint - 100)
        sleep(.001)
        self.setAngle(self.centerpoint)

    def nudgeRight(self):
        self.setAngle(self.centerpoint + 100)
        sleep(.001)
        self.setAngle(self.centerpoint)

    def moveLeft(self):
        self.setAngle(self.centerpoint - 1000)
        sleep(.001)
        self.setAngle(self.centerpoint)

    def moveRight(self):
        self.setAngle(self.centerpoint + 1000)
        sleep(.001)
        self.setAngle(self.centerpoint)

    def resetZero(self, newval):
        self.centerpoint = newval

    def setAngle(self, degrees):
        self.controller.setTarget(self.my_id, degrees)

    def conv(self, degrees):
        pass

class LaunchServo(Servo):
    def __init__(self, my_id):
        """
        my_id = the ID of the servo
        rotation = the max rotation angle that the servo can go to
        initPos = The initial position to place servo at in degrees, defaults to 0
        """
        self.my_id = my_id
        self.controller = control
        self.controller.setRange(self.my_id, 0, 0)
        self.controller.setSpeed(self.my_id, 0)
        self.controller.setAccel(self.my_id, 0)
        self.controller.setRange(self.my_id, 3000, 6000)
        self.controller.setTarget(self.my_id, 3120)

    def launch(self):
        self.controller.setTarget(self.my_id, 5304)
