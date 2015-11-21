import RPi.GPIO as GPIO
from time import sleep
import socket

from time import ctime

PORT = 4444


class Board(object):
    def __init__(self):
        self.GPIO = GPIO
        # self.GPIO.setmode(GPIO.BOARD)
        self.GPIO.setmode(GPIO.BCM)

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


class Motor(object):
    def __init__(self, dir_pin_a, dir_pin_b, speed_pin):
        self.dir_pin_a = dir_pin_a
        self.dir_pin_b = dir_pin_b
        GPIO.setup(self.dir_pin_a, GPIO.OUT)
        GPIO.setup(self.dir_pin_b, GPIO.OUT)

        self.speed_pin = speed_pin
        GPIO.setup(self.speed_pin, GPIO.OUT)
        self.speed_pwm = GPIO.PWM(self.speed_pin, 5000)
        self.speed_pwm.start(0)

    def set(self, speed):
        if speed < 0:
            GPIO.output(self.dir_pin_a, False)
            GPIO.output(self.dir_pin_b, True)
            speed = -speed
        else:
            GPIO.output(self.dir_pin_a, True)
            GPIO.output(self.dir_pin_b, False)
        self.speed_pwm.ChangeDutyCycle(speed)

    def set_feq(self, feq):
        self.speed_pwm.ChangeFrequency(feq)

    def set_brake(self, type):
        if type == 0:
            GPIO.output(self.dir_pin_a, False)
            GPIO.output(self.dir_pin_b, False)
        else:
            GPIO.output(self.dir_pin_a, True)
            GPIO.output(self.dir_pin_b, True)

    def get(self):
        return 0


with Socket() as sock, Board() as GPIO:
    sock.bind(('', PORT))
    led = LED(17)
    # led = LED(25)
    motor1 = Motor(23, 24, 25)

    while True:
        cmd = raw_input('> ').strip()
        if cmd == 'break 0':
            motor1.set_break(0)
        elif cmd == 'break 1':
            motor1.set_break(1)
        elif cmd.split(' ')[0] == 'go':
            motor1.set(int(cmd.split(' ')[1]))
        elif cmd == 'led on':
            led.set(True)
        elif cmd == 'led off':
            led.set(False)
        elif cmd.split(' ')[0] == 'cf':
            motor1.set_feq(int(cmd.split(' ')[1]))
        else:
            print("Error")

        # data, addr = sock.recvfrom(1024)
        # print data, addr
        # if not data:
        #     break
        # # sleep(1)
        # # print led.get()
        # # if data == '1':
        # #     led.set(True)
        # # elif data == '2':
        # #     led.set(False)
        # sleep(1)
        # led.set(True)
