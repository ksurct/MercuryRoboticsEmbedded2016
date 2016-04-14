import spidev
import time
spi = spidev.SpiDev()
spi.open(0, 1)


class IR_sensor:
    p1 = -0.0000000000010569
    p2 = 0.0000000027286
    p3 = -0.0000027447
    p4 = 0.0013672
    p5 = -0.351
    p6 = 41.779

    def __init__(self, sensor_id):
        self.sensor_id = sensor_id
        self.digiFilter = [0]*5
        self.count = 0
        self._value = 0

    def __enter__(self):
        return self

    def __exit__(self, *enc):
        return

    def update(self):
       resp = spi.xfer2([1, (8+self.sensor_id) << 4, 0])
       data  = ((resp[1]&3) << 8) + resp[2]
       temp  = self.p1*data**5 + self.p2*data**4 + self.p3*data**3 + self.p4*data**2 + self.p5*data + self.p6
       self.digiFilter[self.count] = temp
       if (self.count < 4):
           self.count += 1
       else:
           self.count = 0
       self._value = sum(self.digiFilter)/5

    def get(self):
          return self._value
