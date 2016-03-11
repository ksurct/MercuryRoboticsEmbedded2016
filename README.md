# MercuryRoboticsEmbedded2016

Embedded system code for the Mercury Robotics Competition 2016

<http://ksurct.herokuapp.com/>

# Quick start

This should run in unix. Probably will not run on windows.

- Install [python3.5](https://www.python.org/downloads/).
- Create a virtual environment by running `python3.5 -m venv .python-venv`. This creates an isolated python environment with its own set of packages.
- Activate the virtual environment. **You will need to do this every time you open a terminal!**. Run `source ./.python-venv/bin/activate`.
- Install some packages. Run `pip install -r ./requirements.txt`.
- Install protobuf. Follow [these instructions](https://github.com/google/protobuf).  
- Make the protobuf files. Run `make`.
- Install program with `pip install -e .`
- Run the program with `sudo $(which ksurobot) robot`

# Commandline

There is a commandline app for interacting with the robot remotely.

- Run `pip install ptpython`. This will install the excellent ptpython module which is also useful on its own.
- Run `sudo ~/Code/python-venv/bin/ksurobot interact`. This will run initialization put you into a command prompt.

## Usage

- The `r` variable contains the Robot object and the  `s` variable is the Server object, as defined in 'ksurobot/robot.py'. You can, for example, set the right motor speed using `r.motor_right.set(20)`.

# Technical Document

Its in report/main.md.

To update the class diagram:

- Run `pip install pylint`
- Install graphviz
- Run `pyreverse ksurobot -o png`
