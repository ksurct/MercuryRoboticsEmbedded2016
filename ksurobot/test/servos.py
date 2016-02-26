import time
from .hardware.servo import Servo

Servo0 = Servo(0, 180, initPos = 0)
Servo1 = Servo(1, 180, initPos = 0)
Servo2 = Servo(2, 180, initPos = 0)
Servo3 = Servo(3, 180, initPos = 0)
Servo4 = Servo(4, 180, initPos = 0)

for (i = 0; i < 180; i += 10)
    Servo0.setAngle(i))
    time.sleep(1)

time.sleep(5)
Servo1.setAngle(30)
Servo2.setAngle(90)
Servo3.setAngle(60)

time.sleep(5)

Servo4.setAngle(0)
Servo1.setAngle(15)
Servo2.setAngle(0)
