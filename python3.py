#!/usr/bin/env python3

import configargparse
import sys
import os
import logging
import logging.handlers

FORMAT = "%(asctime)s [%(funcName)6s:%(lineno)3d]: %(message)s"
LOG_LEVELS = (logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG)
log = logging.getLogger("RENAME")

# https://stackoverflow.com/a/38458877
class MyStreamHandler(logging.StreamHandler):
    def emit(self,record):
        messages = record.msg.split('\n')
        for message in messages:
            record.msg = message
            super().emit(record)

class MyFileHandler(logging.FileHandler):
    def emit(self,record):
        messages = record.msg.split('\n')
        for message in messages:
            record.msg = message
            super().emit(record)

class MyRotatingFileHandler(logging.handlers.RotatingFileHandler):
    def emit(self,record):
        messages = record.msg.split('\n')
        for message in messages:
            record.msg = message
            super().emit(record)


def main(args):
    log.critical(args)


def get_args():
    parser = configargparse.ArgParser(
        default_config_files = [
            "~/.RENAMErc",
        ],
        description="RENAME"
    )
    parser.add("-d", "--working-dir", default="RENAME",
               help="For logging, and other data")
    parser.add("-v", "--verbose", action="count", default=0)
    parser.add("-l", "--log-file", nargs="?", default=None,
               const=True, help="Where to log.  If not specified, "
               "log to 'WORKING_DIR/log', if specified without an "
               "option, log to stdout, if specified with option, log "
               "to 'LOG_FILE'")
    args = parser.parse_args()

    # It shouldn't matter the value of log_file is after this block
    if args.log_file is None:
        args.log_file = os.path.join(args.working_dir, "log")
        handler = MyRotatingFileHandler(
            args.log_file, maxBytes=2000, backupCount=30)
    elif args.log_file and not isinstance(args.log_file, str):
        args.log_file = "stdout"
        handler = MyStreamHandler(stream=sys.stdout)
    else:
        handler = MyFileHandler(filename=args.log_file)

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
