#!/bin/bash

rsync -va --exclude __pycache__ --exclude .python-venv ./ pi@rpi1.local:code/src
ssh pi@rpi1.local
