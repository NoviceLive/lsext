#!/usr/bin/python3

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#     lsext.py by Novice Live, http://novicelive.org/ :)
#
#     list the different extensions of files in specified directories.
#     to be honest, a shellscript might be more suitable for doing this stuff.
#
#     1. symbolic links will be followed by python's default. no switch to choose currently.
#
#     2. `os.walk' is preferred in next version.
#
#     jan 2 2015
#
#     3. added argument parser and the count functionality (`-c' switch), just like `find -type f -name *.pdf | wc -l'.
#
#     jan 28, 2015
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#     Copyright (C) 2015  Gu Zhengxiong
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import sys
import os
import argparse

ext_list = []
ext_dict = {}

def traverse_ext(cur_dir, count):
    global ext_list
    global ext_dict
    old_dir = os.getcwd()
    os.chdir(cur_dir)
    for i in os.listdir():
        if os.path.isfile(i):
            ext = os.path.splitext(i)[1]
            if ext:
                if count:
                    if ext in ext_dict:
                        ext_dict[ext] += 1
                    else:
                        ext_dict.update({ext:1})
                else:
                    if ext not in ext_list:
                            ext_list.append(ext)
        elif os.path.isdir(i) and not os.path.islink(i):
            traverse_ext(os.path.join(os.getcwd(), i), count)
    os.chdir(old_dir)

def main():
    global ext_list
    global ext_dict
    parser = argparse.ArgumentParser(description='list the different extensions of files in specified directories')
    parser.add_argument('dir_list',
                        metavar='directory_name',
                        nargs='*',
                        help='specify the directory to list')
    parser.add_argument('-c',
                        '--count',
                        dest='count',
                        action='store_const',
                        const=True,
                        default=False,
                        help='also count the total number of every extension')
    parser.add_argument('-r',
                        '--reverse',
                        dest='reverse',
                        action='store_const',
                        const=True,
                        default=False,
                        help='reverse ouput order')
    parser.add_argument('-n',
                        '--name',
                        dest='name',
                        action='store_const',
                        const=True,
                        default=False,
                        help='output order according to extension names rather than numbers')
    
    args = parser.parse_args()

    if args.dir_list:
        for i in args.dir_list:
            if os.path.isdir(i):
                traverse_ext(i, args.count)
                if args.count:
                    print(i + ':', sorted(ext_dict.items(), key=lambda x:x[not args.name], reverse=args.reverse))
                    ext_dict = {}
                else:
                    print('{}: {}'.format(i, sorted(ext_list, reverse=args.reverse)))
                    ext_list = []
            else:
                print('invalid directory name: ', i)
    else:
        traverse_ext(os.getcwd(), args.count)
        if args.count:
            print(sorted(ext_dict.items(), key=lambda x:x[not args.name], reverse= args.reverse ))
        else:
            print(sorted(ext_list, reverse=args.reverse))
    
if __name__ == '__main__':
    main()
