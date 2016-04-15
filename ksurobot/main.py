import argparse
from .util import get_config
from .process_setup import process_setup

DEFAULT_PORT = 9002
DEFAULT_ADDR = 'raspberrypi.local'


def run_basestation(ns):
    from .basestation import main
    main()


def run_robot(ns):
    from .robot import main
    main()


def run_install(ns):
    from .install import main
    main()


def run_interact(ns):
    from .test.interact import main
    main()


parser = argparse.ArgumentParser(prog='ksurobot')
parser.add_argument('--port', default=DEFAULT_PORT)
parser.add_argument('--addr', default=DEFAULT_ADDR)
parser.add_argument('--emulate', action='store_true')

subparser = parser.add_subparsers()

basestation_parser = subparser.add_parser('basestation')
basestation_parser.set_defaults(func=run_basestation)

robot_parser = subparser.add_parser('robot')
robot_parser.set_defaults(func=run_robot)

install_parser = subparser.add_parser('install')
install_parser.set_defaults(func=run_install)

interact_parser = subparser.add_parser('interact')
interact_parser.set_defaults(func=run_interact)


def main():
    process_setup()
    args = get_config()
    args.func(args)
