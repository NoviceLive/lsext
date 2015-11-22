#!/usr/bin/env python3


"""
Copyright 2015 Gu Zhengxiong <rectigu@gmail.com>
"""


import sys
sys.EXIT_SUCCESS = 0
sys.EXIT_FAILURE = 1
import logging
import os
import itertools
from operator import itemgetter

from .cli import parse_args
from .fswalk import walk_directory
from .utils import (
    get_file_ext, get_file_ext_size, stat_print,
    STR_TO_SCALE
)


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
            all_info = walk_directory(
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
                for i in [itemgetter(0)(i)
                          for i in  all_ext_info]
            ]
            unique_exts = sorted(set(all_exts))
            if args.number:
                num = sorted(
                    {
                        i:all_exts.count(i) for i in unique_exts
                    }.items(),
                    key=itemgetter(1),
                    reverse=True)
                stat_print(num, False)
            elif args.size:
                size = {i:0 for i in unique_exts}
                for i in all_ext_size_info:
                    size[str.lower(i[0])] += i[1]
                size = sorted(
                    size.items(), key=itemgetter(1),
                    reverse=True)
                stat_print(size, STR_TO_SCALE[args.human])
            else:
                print((5 * ' ').join(unique_exts))
        else:
            print('could not access: {}\nmay not exist'.format(i))


if __name__ == '__main__':
    sys.exit(main())
