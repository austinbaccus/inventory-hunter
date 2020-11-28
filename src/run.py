import argparse
import locale
import logging
import sys

from config import parse_config
from hunter import hunt


# required for price parsing logic
locale.setlocale(locale.LC_ALL, '')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type=argparse.FileType('r'), default='/config.yaml', help='YAML config file')
    return parser.parse_args()


def main():
    args = parse_args()
    log_level = logging.INFO
    logging.basicConfig(level=log_level, format='{levelname:.1s}{asctime} {message}', style='{')

    try:
        config = parse_config(args.config)
        hunt(args, config)
    except Exception:
        logging.exception('caught exception')
        sys.exit(1)


if __name__ == '__main__':
    main()
