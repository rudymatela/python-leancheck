#!/usr/bin/env python
#
# LeanCheck for Python.  Core module.
#
# (C) 2023-2025  Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)


import itertools
import leancheck.iitertools as ii


# An implementation of the fusc function (EWD 570)
# https://www.cs.utexas.edu/~EWD/ewd05xx/EWD570.PDF
#
# >>> [leancheck._fusc(x) for x in range(24)]
# [0, 1, 1, 2, 1, 3, 2, 3, 1, 4, 3, 5, 2, 5, 3, 4, 1, 5, 4, 7, 3, 8, 5, 7]
def fusc(n):
    a, b = 1, 0
    while n:
        if n % 2 == 0:
            a += b
        else:
            b += a
        n //= 2
    return b


# See _fusc
def fuscs():
    return (fusc(n) for n in itertools.count(1))


# Generates all positive float numbers.
# All pairs n/d are included without repetition in their most simple form.
# This is the Calkin-Wilf sequence
# computed with the help of the fusc function (EWD 570)
def positive_floats():
    return itertools.starmap(lambda n, d: n / d, zip(fuscs(), ii.tail(fuscs())))


def negative_floats():
    return map(lambda x: -x, positive_floats())


def floats():
    yield 0.0
    yield from ii.intercalate(positive_floats(), negative_floats())


# Runs tests if this is not being imported as a module.
if __name__ == "__main__":
    import doctest
    import sys

    (failures, _) = doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)
    if failures:
        sys.exit(1)
