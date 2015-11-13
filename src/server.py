import RPi.GPIO as GPIO
from time import sleep
import socket

from time import ctime

PORT = 4444


class Board(object):
    def __init__(self):
        self.GPIO = GPIO
        self.GPIO.setmode(GPIO.BOARD)

    def __enter__(self):
        return self.GPIO

    def __exit__(self, type, value, tb):
        print "Closing board."
        self.GPIO.cleanup()


class Socket(object):
    def __init__(self):
        self.socket = None

    def __enter__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return self.socket

    def __exit__(self, type, value, tb):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except socket.error as e:
            if e.errno != 107:
                raise


class LED(object):
    def __init__(self, num):
        self.pin = num
        GPIO.setup(self.pin, GPIO.OUT)

    def set(self, state):
        GPIO.output(self.pin, state)

    def get(self):
        return bool(GPIO.input(self.pin))


with Socket() as sock, Board() as GPIO:
    sock.bind(('', PORT))
    led = LED(16)
    
    while True:
        data, addr = sock.recvfrom(1024)
        print data, addr
        if not data:
            break
        # sleep(1)
        # print led.get()
        # if data == '1':
        #     led.set(True)
        # elif data == '2':
        #     led.set(False)
        led.set(not led.get())
