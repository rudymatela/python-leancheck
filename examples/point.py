#!/usr/bin/env python
#
# Using LeanCheck to test a distance function over a point class
#
# (C) 2026  Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)
#
# This illustrates how one can use LeanCheck
# to define custom (global) enumerators.

import leancheck
from leancheck import Enumerator


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def distance(self, other):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2


# or...
# Point = collections.namedtuple('Point', ['x', 'y'])


# # The following is automatically inferred from type annotations:
# Enumerator.register_cons(Point, float, float)


def prop_distance_positive(p: Point, q: Point) -> bool:
    return Point.distance(p, q) >= 0


def prop_self_distance(p: Point) -> bool:
    return Point.distance(p, p) == 0


leancheck.main(verbose=True)
