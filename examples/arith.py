#!/usr/bin/env python
#
# Using LeanCheck to test arithmetic functions
#
# (C) 2023-2024  Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)

from leancheck import check
import leancheck


def prop_commute(x:int, y:int) -> bool:
    return x + y == y + x

# incorrect property
def prop_increase(x:int, y:int) -> bool:
    return x + y > x

# This collects and tests all properties:
leancheck.main(verbose=True, exit_on_failure=False)
# Normal users should just call leancheck.main()
# We set exit_on_failure=False here because we have
# an intentionally incorrect property.
# The verbose is there so we get info on correct properties as well.
