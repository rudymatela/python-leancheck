#!/usr/bin/env python
#
# Using LeanCheck in dump/debug mode
#
# (C) 2023-2026  Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)

import leancheck


def prop_plus_commutes(x: int, y: int) -> bool:
    "'+' is commutative"
    return x + y == y + x


def prop_idempotence(xs: list[int]) -> bool:
    "sorted is idempotent"
    return sorted(sorted(xs)) == sorted(xs)


def prop_and_commutes(p: bool, q: bool) -> bool:
    "'and' is commutative"
    return (p and q) == (q and p)


# The following property is intentionally incorrect
def prop_and_or_interchangeable(p: bool, q: bool) -> bool:
    "'and' and 'or' are interchangeable (intentionally incorrect)"
    return (p and q) == (p or q)


if __name__ == "__main__":
    leancheck.main(dump=12, exit_on_failure=False)
    # failure is expected here  :-)  hence exit_on_failure=False
