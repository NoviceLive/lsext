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

ext_list = []

def traverse_ext(cur_dir):
    global ext_list
    old_dir = os.getcwd()
    os.chdir(cur_dir)
    for i in os.listdir():
        if os.path.isfile(i):
            ext = os.path.splitext(i)[1]
            if ext and ext not in ext_list:
                ext_list.append(ext)
        elif os.path.isdir(i):
            traverse_ext(os.path.join(os.getcwd(), i))
    os.chdir(old_dir)

if __name__ == '__main__':
    no_arg = True
    for i, dir_name in enumerate(sys.argv):
        if i:
            no_arg = False
            if os.path.isdir(dir_name):
                traverse_ext(dir_name)
                print('{}: {}'.format(dir_name, sorted(list)))
                ext_list = []
            else:
                print('invalid directory name: ', dir_name)
    if no_arg:
        traverse_ext(os.getcwd())
        print(sorted(ext_list))
