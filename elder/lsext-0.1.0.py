#!/usr/bin/env python3

"""
file format distribution analyzer

by Novice Live, http://novicelive.org :)

1. rewritten from scratch, using os.walk instead of using recursive os.listdir.

2. added size and number distribution analysis.

3. likely to add the feature of recognizing files based upon their magic numbers rather than the suffixes.
   obviously, this feature will cost more time.

feb 14, 2015

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
import functools
import operator
import argparse

def main():
    parser = argparse.ArgumentParser(description='analyze the distribution of different file formats in specified directories', conflict_handler='resolve')
    parser.add_argument('dirs',
                        metavar='dir',
                        nargs='*',
                        help='the directory to analyze')
    parser.add_argument('-s', '--size',
                        dest='size',
                        action='store_const',
                        const=True,
                        default=False,
                        help='analyze size distribution')
    parser.add_argument('-n', '--number',
                        dest='number',
                        action='store_const',
                        const=True,
                        default=False,
                        help='analyze number distribution')
    parser.add_argument('-h', '--human',
                        dest='human',
                        choices=('k', 'm', 'g'),
                        default='b',
                        help='human-readable size in the specified unit')
    parser.add_argument('-f', '--follow',
                        dest='follow',
                        action='store_const',
                        const=True,
                        default=False,
                        help='follow symbolic links')
    
    args = parser.parse_args()
    
    if not args.dirs:
        args.dirs.append(os.getcwd())
        
    for i in args.dirs:
        if os.path.isdir(i) and os.access(i, os.F_OK | os.R_OK):
            info = get_all_info(i, args.size, args.follow)
            exts = [operator.itemgetter(0)(i) for i in info]
            unique = sorted(set(exts))
            
            if args.number:
                num = sorted({i:exts.count(i) for i in unique}.items(), key=operator.itemgetter(1), reverse=True)
                stat_print(num, False)
            elif args.size:
                size = {i:0 for i in unique}
                for i in info:
                    size[i[0]] += i[1]
                size = sorted(size.items(), key=operator.itemgetter(1), reverse=True)
                stat_print(size, str_to_scale[args.human])
            else:
                print((5 * ' ').join(unique))
        else:
            print('could not access: {}\nmay not exist'.format(i))
            
str_to_scale = {'b':1, 'k':1024, 'm':1024 * 1024, 'g':1024 * 1024 * 1024}

scale_to_str = {1:'B', 1024:'KiB', 1024 * 1024:'MiB', 1024 * 1024 * 1024:'GiB'}
            
def stat_print(source, scale):
    """
    print all keys in the specified dictionary with consideration of the weight of its value
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

def get_all_info(directory, has_size, follow):
    """
    obtain raw extension and maybe size information for further processing
    """
    return functools.reduce(
        operator.concat,
        [
            [
                ((lambda x: os.path.splitext(x)[1])(j), os.path.getsize(os.path.join(i[0], j)) if has_size else None)
                for j in i[2]
            ]
            for i in os.walk(directory, followlinks=follow)
        ])

if __name__ == '__main__':
    main()
