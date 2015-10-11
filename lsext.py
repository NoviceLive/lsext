#!/usr/bin/env python3


"""
Copyright 2015 Gu Zhengxiong <rectigu@gmail.com>
"""


__version__ = 'lsext 0.1.0'


import sys
sys.EXIT_SUCCESS = 0
sys.EXIT_FAILURE = 1
import argparse
import logging
import os
import itertools
import operator

import fswalk


def main():
    """
    Start hacking.
    """
    args = parse_args()
    logging.basicConfig(
        format='%(levelname)-11s: %(message)s',
        level={
            0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG
        }[args.verbose % 3])

    for i in args.dirs:
        if os.path.isdir(i) and os.access(i, os.F_OK | os.R_OK):
            logging.info("%s: ", i)
            all_info = fswalk.walk_directory(
                i,
                get_file_ext if not args.size else get_file_ext_size,
                args.ignore if args.ignore else (),
                args.follow)
            # need two independent generators
            # if we still want to extract size information.
            all_ext_info, all_ext_size_info = itertools.tee(
                all_info) if args.size else (all_info, None)
            all_exts = [
                str.lower(i) for i in all_ext_info
            ] if not args.size else [
                str.lower(i)
                for i in [operator.itemgetter(0)(i)
                          for i in  all_ext_info]
            ]
            unique_exts = sorted(set(all_exts))
            if args.number:
                num = sorted(
                    {
                        i:all_exts.count(i) for i in unique_exts
                    }.items(),
                    key=operator.itemgetter(1),
                    reverse=True)
                stat_print(num, False)
            elif args.size:
                size = {i:0 for i in unique_exts}
                for i in all_ext_size_info:
                    size[str.lower(i[0])] += i[1]
                size = sorted(
                    size.items(), key=operator.itemgetter(1),
                    reverse=True)
                stat_print(size, str_to_scale[args.human])
            else:
                print((5 * ' ').join(unique_exts))
        else:
            print('could not access: {}\nmay not exist'.format(i))


str_to_scale = {
    'b':1,
    'k':1024,
    'm':1024 * 1024,
    'g':1024 * 1024 * 1024
}

scale_to_str = {
    1:'B',
    1024:'KiB',
    1024 * 1024:'MiB',
    1024 * 1024 * 1024:'GiB'
}


def get_file_ext(file_path):
    """
    Get the extension of the file.
    """
    return os.path.splitext(file_path)[1]


def get_file_size(filename):
    """
    Get the size of the file.
    """
    if os.path.islink(filename):
        return 0
    return os.path.getsize(filename)


def get_file_ext_size(file_path):
    """
    Get the extension and size of the file.
    """
    return get_file_ext(file_path), get_file_size(file_path)


def stat_print(source, scale):
    """
    Print with their weight.
    """
    total = sum(operator.itemgetter(1)(i) for i in source)
    for i in source:
        print(
            "{:20} {:<20}{:10} {:<10.2%}".format(
                i[0], round(i[1] / scale, 4) if scale else i[1],
                scale_to_str[scale] if scale else '', i[1] / total))


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


if __name__ == '__main__':
    sys.exit(main())
