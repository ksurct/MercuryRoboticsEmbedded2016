#
from ._maestro import Controller
control = Controller()

class Servo:

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
        #TODO Test to see if the position of the servo in relation to the pulse
        #     width is linear or not
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
        #TODO Check to make sure these values are correct
        return int(self.x + degrees * ((self.y - self.x)/(90)))
