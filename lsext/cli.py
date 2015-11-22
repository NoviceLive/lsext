"""
Copyright 2015 Gu Zhengxiong <rectigu@gmail.com>
"""


__version__ = 'lsext 0.1.0'


import argparse
import os


def parse_args():
    """
    Parse the arguments.
    """
    parser = argparse.ArgumentParser(
        description="Analyze The Distribution Of File Formats",
        conflict_handler='resolve')
    parser.add_argument(
        'dirs', metavar='dir', nargs='*', default=[os.getcwd()],
        help='The directory to analyze')
    parser.add_argument(
        '-s', '--size', dest='size', action='store_true',
        help='Analyze size distribution')
    parser.add_argument(
        '-n', '--number', dest='number', action='store_true',
        help='Analyze number distribution')
    parser.add_argument(
        '-h', '--human',
        dest='human', choices=('k', 'm', 'g'), default='b',
        help='Human-readable size in the specified unit')
    parser.add_argument(
        '-f', '--follow', dest='follow', action='store_true',
        help='Follow symbolic links')
    parser.add_argument(
        '-i', '--ignore', dest='ignore', nargs='+',
        help='Ignore the specified directory names')
    parser.add_argument(
        '-v', '--verbose', action='count', default=0,
        help='turn on verbose mode, -vv for debugging mode')
    parser.add_argument(
        '-V', '--version', action='version', version=__version__)
    return parser.parse_args()
