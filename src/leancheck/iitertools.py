#!/usr/bin/env python
#
# LeanCheck for Python.  iitertools module.
#
# (C) 2023-2026  Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)
"""
This is part of the [LeanCheck package](https://pypi.org/project/leancheck/):
an enumerative property-based testing library for Python.

This module defines some utilities for manipulating tiered generators.
Please see the `Enumerator` class for a nicer interface.

You are better off importing the main `leancheck` module
with `import leancheck`.
"""


# TODO: document these functions


import itertools


def nest(xs):
    for x in xs:
        yield [x]


def flatten(xss):
    for xs in xss:
        yield from xs


def unit(x):
    yield [x]


def intercalate(generator1, generator2):
    """
    This function intercalates the two given iterables.

    >>> list(intercalate([1,2,3], [-1, -2, -3]))
    [1, -1, 2, -2, 3, -3]

    If the arguments are generators, they will be consumed.

    >>> list(intercalate((x for x in [1,2,3]), (y for y in [4,5,6])))
    [1, 4, 2, 5, 3, 6]
    """
    g1 = (x for x in generator1)  # makes this work on lists
    g2 = (y for y in generator2)  # makes this work on lists
    while True:
        try:
            yield next(g1)
        except StopIteration:
            yield from g2
            break
        try:
            yield next(g2)
        except StopIteration:
            yield from g1
            break


def zippend(*iiterables):
    return map(
        list,
        itertools.starmap(itertools.chain, itertools.zip_longest(*iiterables, fillvalue=[])),
    )


def pproduct(xss, yss, with_f=None):
    if with_f is None:
        with_f = lambda x, y: (x, y)
    xss_ = []
    yss_ = []
    l = 0
    while True:
        xss_.append(list(next(xss, [])))
        yss_.append(list(next(yss, [])))
        l += 1
        zs = []
        for i in range(0, l):
            zs += [with_f(x, y) for x in xss_[i] for y in yss_[l - i - 1]]
        if zs == []:
            # This is "sound-but-incomplete".
            # TODO: in the final version, use None as a default value
            # in the appends above
            # and break only in the case where we
            # end up with empty zs because of None values
            # there's an opportunity for memory optimization here
            # such as in the example of product between integers and booleans
            break
        yield zs


def delay(xss):
    yield []
    yield from xss


def mmap(f, xss):
    for xs in xss:
        yield [f(x) for x in xs]


def ffilter(p, xss):
    for xs in xss:
        yield [x for x in xs if p(x)]


def cconcat(xssss):
    # cconcat([ [xss0, yss0, zss0, ...]
    #         , [xss1, yss1, zss1, ...]
    #         , [xss2, yss2, zss2, ...], ...
    #         ])
    yss = []
    xsss = map(lambda xsss: zippend(*xsss), xssss)
    # xsss = [ xyss0, xyss1, xyss2, ...]
    for xss in xsss:
        yss = zippend(yss, xss)
        ys = list(next(yss, []))
        yield ys
    yield from yss


def cconcatmap(f, xss):
    return cconcat(mmap(f, xss))


def listss(mkTiers):
    yield [[]]
    yield from pproduct(mkTiers(), listss(mkTiers), with_f=lambda x, xs: [x] + xs)


def tail(gen):
    return itertools.islice(gen, 1, None)


# --- debugging tools, may be removed without warning ---
def llist(gen):
    return list(map(list, gen))


def lllist(gen):
    return list(map(llist, gen))


def llllist(gen):
    return list(map(lllist, gen))


# Runs tests if this is not being imported as a module.
if __name__ == "__main__":
    import doctest
    import sys

    (failures, _) = doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)
    if failures:
        sys.exit(1)
