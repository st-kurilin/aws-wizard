import argparse
import logging
import sys

from . import cmdserver
from . import cmdstaticweb

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AWS made easy.')
    parser.add_argument('--verbose', '-V', help='Give more output.', action="store_true", default=False)
    commands_parser = parser.add_subparsers(help='commands')

    cmdstaticweb.register_commands(commands_parser)
    cmdserver.register_commands(commands_parser)

    args = parser.parse_args()  # can terminate execution when HELP called or parsing failed
    logging.basicConfig(level=(logging.DEBUG if args.verbose else logging.WARNING))

    if cmdstaticweb.exec_command(sys.argv, args):
        pass
    elif cmdserver.exec_command(sys.argv, args):
        pass
    else:
        raise Exception("Failed to parse arguments.\nTo get assistance run "
                        "'python -m awswizard -h' or visit aws-wizard.com ")