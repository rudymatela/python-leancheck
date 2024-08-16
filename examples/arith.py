#!/bin/bash
#
# Using LeanCheck to test arithmetic functions
#
# (C) 2023-2024  Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)

from leancheck import check


def prop_commute(x:int, y:int) -> bool:
    return x + y == y + x

# incorrect property
def prop_increase(x:int, y:int) -> bool:
    return x + y > x


# should pass
check(prop_commute)

# should fail
check(prop_increase)
