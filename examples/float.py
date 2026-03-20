#!/usr/bin/env python
#
# Using LeanCheck to test functions over floats
#
# (C) 2023-2024  Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)

from leancheck import *
import leancheck
import math


def prop_commute(x: float, y: float) -> bool:
    return x + y == y + x


# this fails when math.inf is included in the float enumeration!
def prop_inc_monotonic(x: float) -> bool:
    return x + 1 > x


def prop_subadd(x: float, y:float) -> bool:
    return x - y + y == x


def prop_subadd_correct(x: float, y:float) -> bool:
    return math.isclose(x - y + y, x)


def prop_divmul(x: float, y:float) -> bool:
    precondition(y)
    return x / y * y == x


leancheck.main(verbose=True, exit_on_failure=False, max_tests=1080)
