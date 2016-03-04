#
from ._maestro import Controller
control = Controller()

class Servo(object):

    def __init__(self, my_id, rotation, initPos = 0, x = 3990):
        """
        my_id = the ID of the servo
        rotation = the max rotation angle that the servo can go to
        initPos = The initial position to place servo at in degrees, defaults to 0
        x = the "0" position of the servo in quarter-microseconds
        """
        self.my_id = my_id
        self.controller = control
        self.x = x
        self.y = 7910
        self.controller.setRange(self.my_id, 0, 0)
        self.controller.setSpeed(self.my_id, 0)
        self.controller.setAccel(self.my_id, 0)
        self.setAngle(initPos)

    def setAngle(self, degrees):
        self.controller.setTarget(self.my_id, self.conv(degrees))

    def setTarget(self, target):
        self.controller.setTarget(self.my_id, target)

    def getPos(self):
        return self.controller.getPosition(self.my_id)

    def isMoving(self):
        return self.controller.isMoving(self.my_id)

    def getMyID(self):
        return self.my_id;

    def conv(self, degrees):
        return int(self.x + degrees * ((self.y - self.x)/(90)))

class TitaniumServo(Servo):

    def __init__(self, my_id, rotation, initPos = 0):
        """
        my_id = the ID of the servo
        rotation = the max rotation angle that the servo can go to
        initPos = The initial position to place servo at in degrees, defaults to 0
        """
        self.my_id = my_id
        self.controller = control
        self.x = 4000
        self.y = 8000
        self.controller.setRange(self.my_id, 0, 0)
        self.controller.setSpeed(self.my_id, 0)
        self.controller.setAccel(self.my_id, 0)
        self.setAngle(initPos)

    def setAngle(self, degrees):
        self.controller.setTarget(self.my_id, self.conv(degrees))

    def conv(self, degrees):
        return int(self.x + 42 * degrees)
