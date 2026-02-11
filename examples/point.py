#!/usr/bin/env python
#
# Using LeanCheck to test a distance function over a point class
#
# (C) 2025  Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)
#
# This illustrates how one can use LeanCheck
# to define custom (global) enumerators.
#
# type: ignore  # TODO: XXX: FIXME: avoid this mypy hint

import leancheck
from leancheck import Enumerator


class Point:
    x: float  # float | int ?, cf. [1]
    y: float  # float | int ?

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def distance(self, other):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2


# or...
# Point = collections.namedtuple('Point', ['x', 'y'])


# TODO: make so that the following is inferred from types?
Enumerator.register(Point, Enumerator.cons(Point, int, int))


def prop_distance_positive(p: Point, q: Point) -> bool:
    return Point.distance(p, q) >= 0


def prop_self_distance(p: Point) -> bool:
    return Point.distance(p, p) == 0


leancheck.main(verbose=True)

# Interesting discussion:
# [1]: https://stackoverflow.com/questions/50928592/mypy-type-hint-unionfloat-int-is-there-a-number-type
