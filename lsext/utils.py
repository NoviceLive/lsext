"""
Copyright 2015 Gu Zhengxiong <rectigu@gmail.com>
"""


import os
from operator import itemgetter


def removemany(old, values):
    """
    Remove many values from a list.
    """
    for i in values:
        if i in old:
            old.remove(i)


STR_TO_SCALE = {
    'b':1,
    'k':1024,
    'm':1024 * 1024,
    'g':1024 * 1024 * 1024
}

SCALE_TO_STR = {
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
    total = sum(itemgetter(1)(i) for i in source)
    for i in source:
        print(
            "{:20} {:<20}{:10} {:<10.2%}".format(
                i[0], round(i[1] / scale, 4) if scale else i[1],
                SCALE_TO_STR[scale] if scale else '', i[1] / total))
