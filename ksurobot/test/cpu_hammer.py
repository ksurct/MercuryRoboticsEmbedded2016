from multiprocessing import Pool
from math import sqrt


def consume(num):
    print('Thread {}'.format(num))
    for x in range(30000000000):
        sqrt(x)


pool = Pool(processes=4)
pool.map(consume, range(4))
