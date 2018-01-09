#!/usr/bin/env python3

import argparse
import sys
import os
import logging

FORMAT = "%(asctime)s [%(funcName)6s:%(lineno)3d]: %(message)s"
LOG_LEVELS = (logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG)
log = logging.getLogger("RENAME")


def main(args):
    log.critical(args)


def get_args():
    parser = argparse.ArgumentParser(description="RENAME")
    parser.add_argument("-d", "--working-dir", default="RENAME",
                        help="For logging, and other data")
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument("-l", "--log-file", nargs="?", default=None,
                        const=True, help="Where to log.  If not specified, "
                        "log to 'WORKING_DIR/log', if specified without an "
                        "option, log to stdout, if specified with option, log "
                        "to 'LOG_FILE'")
    args = parser.parse_args()

    # It shouldn't matter the value of log_file is after this block
    if args.log_file is None:
        args.log_file = os.path.join(args.working_dir, "log")
        handler = logging.handlers.RotatingFileHandler(
            args.log_file, maxBytes=2000, backupCount=30)
    elif args.log_file and not isinstance(args.log_file, str):
        args.log_file = "stdout"
        handler = logging.StreamHandler(stream=sys.stdout)
    else:
        handler = logging.FileHandler(filename=args.log_file)

    handler.setFormatter(logging.Formatter(FORMAT))
    args.verbose = min([args.verbose, 3])
    handler.setLevel(LOG_LEVELS[args.verbose])
    log.addHandler(handler)

    return args


if __name__ == '__main__':
    try:
        exit(main(get_args()))
    except KeyboardInterrupt as e:
        log.error("\nOperation cancelled.")
