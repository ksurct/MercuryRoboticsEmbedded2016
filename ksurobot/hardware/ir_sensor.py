import spidev
import time
spi = spidev.SpiDev()
spi.open(0,0)
digiFilter = [0]*5
count = 0
p1 = -0.0000000000010569
p2 = 0.0000000027286
p3 = -0.0000027447
p4 = 0.0013672
p5 = - 0.351
p6 = 41.779

while True:
   resp = spi.xfer2([1, 8 << 4, 0])
   data  = ((resp[1]&3) << 8) + resp[2]
   temp  = p1*data**5 + p2*data**4 + p3*data**3 + p4*data**2 + p5*data + p6 
   digiFilter[count] = temp
   if (count < 4):
       count += 1
   else:
       count = 0
   avg = sum(digiFilter)/5
   time.sleep(2)
