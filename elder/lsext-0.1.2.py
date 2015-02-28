#!/usr/bin/env python3

"""
file format distribution analyzer

by Novice Live, http://novicelive.org :)

1. rewritten from scratch, using os.walk instead of using recursive os.listdir.

2. added size and number distribution analysis.

3. likely to add the feature of recognizing files based upon their magic numbers rather than the suffixes.
   obviously, this feature will cost more time.

feb 14, 2015

1. changed to returning chained generators, instead of a list reduced from a list of lists;
   in the the core function `get_all_info'.

2. please refactor the core function `get_all_info', such that,
   you can just collect the information specified by the extracting function which is provided as one of the arguments to `get_all_info'.
   but now i am too exhausted. i have to sleep. let's fix it tomorrow.

feb 19, 2015 happy chinese new year! am i a hard-working and responsible employee, one who still keeps coding to deep night even in the new year's day.

1. completed the refactoring in the core function, `get_all_info'.

feb 20, 2015

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
            all_info = get_all_info(i, get_file_ext if not args.size else get_file_ext_size, args.follow)

            # need two independent generators if we still want to extract size information
            all_ext_info, all_ext_size_info = itertools.tee(all_info) if args.size else (all_info, None)
            
            all_exts = list(all_ext_info) if not args.size else list(map(operator.itemgetter(0), all_ext_info))
            
            unique_exts = sorted(set(all_exts))
            
            if args.number:
                num = sorted({i:all_exts.count(i) for i in unique_exts}.items(), key=operator.itemgetter(1), reverse=True)
                stat_print(num, False)
                
            elif args.size:
                size = {i:0 for i in unique_exts}
                for i in all_ext_size_info:
                    size[i[0]] += i[1]
                size = sorted(size.items(), key=operator.itemgetter(1), reverse=True)
                stat_print(size, str_to_scale[args.human])
                
            else:
                print((5 * ' ').join(unique_exts))
                
        else:
            print('could not access: {}\nmay not exist'.format(i))
            
str_to_scale = {'b':1, 'k':1024, 'm':1024 * 1024, 'g':1024 * 1024 * 1024}

scale_to_str = {1:'B', 1024:'KiB', 1024 * 1024:'MiB', 1024 * 1024 * 1024:'GiB'}

# note using compose_function is surely slower than directly using f(g(x))
compose_function = lambda f, g: lambda x: f(g(x))
get_file_ext = compose_function(operator.itemgetter(1), os.path.splitext)

get_file_size = os.path.getsize

map_function = lambda f, g: lambda x: (f(x), g(x))
get_file_ext_size = map_function(get_file_ext, get_file_size)
            
def stat_print(source, scale):
    """
    print all keys in the specified dictionary with consideration of the weight of its value.
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

def get_all_info(directory, get_info_func, follow):
    """
    obtain the information of all files in a directory.
    which information to extract depends on the specified argument `get_info_func'.

    you can easily adapt this functon into a function which performs the specified operations upon all files in the specified directory, and returns the results.
    actually, it may be more reasonable. e.g. operate_all_files(directory, operation_func, follow).
    """
    return itertools.chain(
        *(
            (
                # need this lambda application to introduce an independent namespace,
                # to avoid the undesired results caused by the undesired lazy evaluation of generator expressions.
                (lambda x: (get_info_func(os.path.join(x[0], i)) for i in x[2]))
                (i)
            )
            for i in os.walk(directory, followlinks=follow)
        )
    )

if __name__ == '__main__':
    main()