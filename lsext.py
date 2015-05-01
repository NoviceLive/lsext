#!/usr/bin/env python3


"""
file format distribution analyzer

by Novice Live, http://novicelive.org :)

Copyright (C) 2015  Gu Zhengxiong

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


import os
import sys
import itertools
import operator
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="""
analyze the distribution of different file formats in specified directories
""",
        conflict_handler='resolve')

    parser.add_argument('dirs', metavar='dir', nargs='*',
                        help='the directory to analyze')
    parser.add_argument('-s', '--size', dest='size', action='store_true',
                        help='analyze size distribution')
    parser.add_argument('-n', '--number', dest='number', action='store_true',
                        help='analyze number distribution')
    parser.add_argument('-h', '--human', dest='human', choices=('k', 'm', 'g'),
                        default='b',
                        help='human-readable size in the specified unit')
    parser.add_argument('-f', '--follow', dest='follow', action='store_true',
                        help='follow symbolic links')
    parser.add_argument('-i', '--ignore', dest='ignore',
                        nargs='+',
                        help='ignore the specified directory names')

    args = parser.parse_args()

    if not args.dirs:
        args.dirs.append(os.getcwd())

    for i in args.dirs:
        if os.path.isdir(i) and os.access(i, os.F_OK | os.R_OK):
            print("{}: ".format(i))

            all_info = operate_all_files(i,

                                         get_file_ext
                                         if not args.size else
                                         get_file_ext_size,

                                         args.follow,
                                         args.ignore if args.ignore else ()
            )

            # need two independent generators
            # if we still want to extract size information.

            all_ext_info, all_ext_size_info = itertools.tee(
                all_info
            ) if args.size else (
                all_info, None
            )

            # treat extensions' cases insignificant.
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
                    # remember treating extensions' cases insignificant.
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


# note using fcompose is surely slower than directly using f(g(x)).
# but the direct form is not always applicable to all scenarios.
fcompose = lambda f, g: lambda x: f(g(x))


get_file_ext = fcompose(operator.itemgetter(1), os.path.splitext)


get_file_size = os.path.getsize


# fcombine or fmap?
fmap = lambda f, g: lambda x: (f(x), g(x))


get_file_ext_size = fmap(get_file_ext, get_file_size)


def stat_print(source, scale):
    """
    print all keys in the specified dictionary
    with consideration of the weight of its value.
    """
    total = sum(map(operator.itemgetter(1), source))
    [
        print("{:20} {:<20}{:10} {:<10.2%}".format(
            i[0],
            round(i[1] / scale, 4) if scale else i[1],
            scale_to_str[scale] if scale else '',
            i[1] / total)
          )
        for i in source
    ]
    return


# def remove_items(old, items):
#     # use list comprehension to loop over a list, but discard the results.
#     # did this waste anything?
#     # or is there any other better ways? (excluding a for loop.)
#     [old.remove(i) for i in items if i in old]
#     return old


def operate_all_files(directory, operation_func, follow, ignore_dirs):
    """
    perform the operation specified by `operation_func'
    upon all files in the specified directory and its subdirectories,
    recursively,
    excluding those in directoies whose name are specified in `ignore_dirs'.
    """
    return itertools.chain(
        *(
            # introduce an independent namespace
            # to avoid the undesired results caused by
            # the undesired lazy evaluation of generator expressions.
            (
                lambda x: (
                    operation_func(os.path.join(x[0], i))
                    for i in x[2]
                )
            )
            (
                # update the directory list
                # which will be traversed later by os.walk
                # to let os.walk ignore the specified directory names
                (lambda x: (
                    x[0],
                    # removed the function `remove_items',
                    # thus making it more unpythonic
                    list(map(x[1].remove, set(ignore_dirs) & set(x[1]))),
                    x[2]))
                (i)
            )
            # topdown=True is, in fact, default, merely for emphasis
            for i in os.walk(directory, topdown=True, followlinks=follow)
        )
    )


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('[!] user cancelled')
