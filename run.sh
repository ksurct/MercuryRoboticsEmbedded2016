#!/bin/bash

rsync -pthrvz src pi@raspberrypi.local:/home/pi/code
ssh pi@raspberrypi.local
