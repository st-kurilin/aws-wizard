import argparse
import logging

from . import cmdstaticweb


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AWS made easy.')
    parser.add_argument('--verbose', '-V', help='Give more output.', action="store_true", default=False)
    subparsers = parser.add_subparsers(help='commands')

    cmdstaticweb.register_commands(commands)

    args = parser.parse_args()  #can terminate execution when HELP called or parsing failed
    logging.basicConfig(level=(logging.DEBUG if args.verbose else logging.WARNING))

    executed = cmdstaticweb.exec_command(args)
    if not executed:
        raise Exception("Failed to parse arguments.\nTo get assistance run "
                        "'python -m awswizard -h' or visit aws-wizard.com ")
