from time import time, sleep
from queue import deque
from math import log

MEMORY = 10

a  = deque([0] * MEMORY)

def calculate():
    total = 0
    time = a.popleft()
    for i, old_time in enumerate(a):
        dtime = old_time - time
        time = old_time
        total += dtime / (3**(MEMORY-i))

    print(total)


for x in range(MEMORY):
    sleep(.1)
    a.append(time())
    a.popleft()

for x in range(20):
    sleep(.1)
    a.append(time())
    calculate()

print('-- .2')

for x in range(20):
    sleep(.2)
    a.append(time())
    calculate()

print('-- .5')

for x in range(20):
    sleep(.5)
    a.append(time())
    calculate()

sleep(9)
for x in range(1):
    a.append(time())
    calculate()






# total = 0
# for x in range(20):
#     d = 10 / (2**(20-x))
#     print(d)
#     total += d
#
# print('--', total)
