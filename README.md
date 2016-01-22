# MercuryRoboticsEmbedded2016
Embedded system code for the Mercury Robotics Competition 2016

http://ksurct.herokuapp.com/

# Quick start
This should run in unix. Probably will not run on windows.

- Install [python3.5](https://www.python.org/downloads/).
- Create a virtual environment by running `python3.5 -m venv .python-venv`.
  This creates an isolated python environment with its own set of packages.
- Activate the virtual environment. __You will need to do this every time
  you open a terminal!__. Run `source ./.python-venv/bin/activate`.
- Install some packages. Run `pip install -r ./requirements.txt`.
- Install protobuf. Follow [these instructions](https://github.com/google/protobuf).  
- Make the protobuf files. Run `make`.
- Run the program with `python -m robot`

# Commandline
There is a commandline app for interacting with the robot remotely.

## Usage
- Run `pip install ptpython`. This will install the excellent ptpython module,
  which is also useful on its own.
- Run `python -m robot.test.interact`. This will start the commandline. It is
  just the python commandline with features from ptpython and some helper functions.
- Use `ws.connect()` to connect to the server. `ws.send(msg)` to send messages to the 
  server.
