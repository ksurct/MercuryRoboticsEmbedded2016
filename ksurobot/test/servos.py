import time
from ksurobot.hardware.servo import *



TestServo = ContinuousServo(3)

for i in range(5000,7000):
    TestServo.setAngle(i)
    print(i)
    time.sleep(.001)

exit()
