import time
from ksurobot.hardware.servo import Servo



TestServo = Servo(0, 3000)

for i in range(4000,9000):
    TestServo.setTarget(i)
    print(i)
    time.sleep(.001)

exit()
