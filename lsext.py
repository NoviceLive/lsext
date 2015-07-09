#!/usr/bin/env python3


"""
File Format Distribution Analyzer

Copyright 2015 Gu Zhengxiong <rectigu@gmail.com>

GPL
"""


import os
import sys
import itertools
import operator
import argparse


def main(args):
    if not args.dirs:
        args.dirs.append(os.getcwd())

    for i in args.dirs:
        if os.path.isdir(i) and os.access(i, os.F_OK | os.R_OK):
            print("{}: ".format(i))

            all_info = operate_all_files(
                i,
                get_file_ext if not args.size else get_file_ext_size,
                args.ignore if args.ignore else (),
                args.follow
            )

            # need two independent generators
            # if we still want to extract size information.
            all_ext_info, all_ext_size_info = itertools.tee(
                all_info
            ) if args.size else (
                all_info, None
            )

            all_exts = list(
                map(str.lower, all_ext_info)
            ) if not args.size else list(
                map(fcompose(str.lower, operator.itemgetter(0)), all_ext_info)
            )

            unique_exts = sorted(set(all_exts))

            if args.number:
                num = sorted(
                    {i:all_exts.count(i) for i in unique_exts}.items(),
                    key=operator.itemgetter(1),
                    reverse=True
                )
                stat_print(num, False)

            elif args.size:
                size = {i:0 for i in unique_exts}

                for i in all_ext_size_info:
                    size[str.lower(i[0])] += i[1]
                size = sorted(
                    size.items(),
                    key=operator.itemgetter(1),
                    reverse=True
                )
                stat_print(size, str_to_scale[args.human])

            else:
                print((5 * ' ').join(unique_exts))

        else:
            print('could not access: {}\nmay not exist'.format(i))


str_to_scale = {'b':1, 'k':1024, 'm':1024 * 1024, 'g':1024 * 1024 * 1024}


scale_to_str = {1:'B', 1024:'KiB', 1024 * 1024:'MiB', 1024 * 1024 * 1024:'GiB'}


fcompose = lambda f, g: lambda x: f(g(x))


get_file_ext = fcompose(operator.itemgetter(1), os.path.splitext)


def get_file_size(filename):
    if os.path.islink(filename):

        return 0

    return os.path.getsize(filename)


fmap = lambda f, g: lambda x: (f(x), g(x))


get_file_ext_size = fmap(get_file_ext, get_file_size)


def stat_print(source, scale):
    total = sum(map(operator.itemgetter(1), source))

    for i in source:
        print("{:20} {:<20}{:10} {:<10.2%}".format(
            i[0],
            round(i[1] / scale, 4) if scale else i[1],
            scale_to_str[scale] if scale else '',
            i[1] / total)
        )


def operate_all_files(path, func, ignored, followlinks):
    return map(func, listdirrec(path, ignored, followlinks))


def listdirrec(path='.', ignored=(), followlinks=False):
    ret = iter(())
    for i in os.walk(path, followlinks=followlinks):
        removemany(i[1], ignored)
        ret = itertools.chain(
            ret,
            (lambda x: (os.path.join(x[0], i) for i in x[2]))(i)
        )

    return ret


def removemany(old, values):
    for i in values:
        if i in old:
            old.remove(i)

def parse_args():
    parser = argparse.ArgumentParser(
        description="""
Analyze The Distribution Of Different File Formats In Specified Directories
""",
        conflict_handler='resolve')

    parser.add_argument('dirs', metavar='dir', nargs='*',
                        help='The directory to analyze')
    parser.add_argument('-s', '--size', dest='size', action='store_true',
                        help='Analyze size distribution')
    parser.add_argument('-n', '--number', dest='number', action='store_true',
                        help='Analyze number distribution')
    parser.add_argument('-h', '--human', dest='human', choices=('k', 'm', 'g'),
                        default='b',
                        help='Human-readable size in the specified unit')
    parser.add_argument('-f', '--follow', dest='follow', action='store_true',
                        help='follow symbolic links')
    parser.add_argument('-i', '--ignore', dest='ignore',
                        nargs='+',
                        help='Ignore the specified directory names')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    try:
        main(args)
    except KeyboardInterrupt:
        print('[!] user cancelled')
