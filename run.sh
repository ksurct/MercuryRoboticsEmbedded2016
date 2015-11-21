#!/bin/bash

rsync -pthrvz --delete --exclude __pycache__ src pi@raspberrypi.local:/home/pi/code
ssh pi@raspberrypi.local
