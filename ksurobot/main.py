import argparse


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
    args = parser.parse_args()
    args.func(args)
