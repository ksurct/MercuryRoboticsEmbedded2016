# MercuryRoboticsEmbedded2016
Embedded system code for the Mercury Robotics Competition 2016

http://ksurct.herokuapp.com/

# Quick start
This should run in unix. Will not run on windows.

- `cd` into 'MercuryRoboticsEmbedded2016'
- Run `./first_time_setup.sh`. This will take a while to run. Be cautious about
  running this on a personal machine.
- Activate the virtual environment. __You will need to do this every time
  you open a terminal!__. Run `source ./installer/_build/virtualenv/bin/activate`.
- Make the protobuf files. Run `make`.
- Run the program with `sudo $(which ksurobot) robot`

# Development

- Activate the virtualenv.
- Run `pip install -r requirements.txt`. This will install python packages used in
  development.

# Commandline
There is a commandline app for interacting with the robot remotely.
- Run `pip install ptpython`. This will install the excellent ptpython module
  which is also useful on its own.
- Run `sudo ~/Code/MercuryRoboticsEmbedded2016/installer/_build/virtualenv/bin/ksurobot interact`.
  This will run initialization put you into a command prompt.

## Usage
- The `r` variable contains the Robot object and the  `s` variable is the
  Server object, as defined in 'ksurobot/robot.py'. You can, for example,
  set the right motor speed using `r.motor_right.set(20)`.
