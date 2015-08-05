"""
Copyright 2015 Gu Zhengxiong <rectigu@gmail.com>
"""


import os
import itertools
import operator


def visit_all_files(path, func, ignored, followlinks):
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
