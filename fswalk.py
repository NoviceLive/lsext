"""
Copyright 2015 Gu Zhengxiong <rectigu@gmail.com>
"""


import os
import itertools


def walk_directory(path, func, ignored, followlinks):
    """
    Walk the directory with the given function.
    """
    return (func(i) for i in listdirrec(path, ignored, followlinks))


def listdirrec(path='.', ignored=(), followlinks=False):
    """
    List the directory recursively.
    """
    ret = []
    for i in os.walk(path, followlinks=followlinks):
        removemany(i[1], ignored)
        ret = itertools.chain(
            ret,
            (lambda x: (os.path.join(x[0], i) for i in x[2]))(i))
    return ret


def removemany(old, values):
    """
    Remove many values from a list.
    """
    for i in values:
        if i in old:
            old.remove(i)
