import spidev
import time
spi = spidev.SpiDev()
spi.open(0,0)
class IR_sensor:
    p1 = -0.0000000000010569
    p2 = 0.0000000027286
    p3 = -0.0000027447
    p4 = 0.0013672
    p5 = - 0.351
    p6 = 41.779

    def __init__(self, sensor_id):
        self.sensor_id = sensor_id
        self.digiFilter = [0]*5
        self.count = 0
        self._value = 0

    def __enter__(self):
        return self

    def update(self):
       resp = spi.xfer2([1, (8+self.sensor_id) << 4, 0])
       data  = ((resp[1]&3) << 8) + resp[2]
       temp  = p1*data**5 + p2*data**4 + p3*data**3 + p4*data**2 + p5*data + p6
       self.digiFilter[count] = temp
       if (self.count < 4):
           self.count += 1
       else:
           self.count = 0
       self._value = sum(self.digiFilter)/5

    def getValue(self):
          return self._value

    def __exit__(self,*enc):
        return
