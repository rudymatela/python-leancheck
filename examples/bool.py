#!/usr/bin/env python
#
# Using LeanCheck to test boolean functions
#
# (C) 2023-2024  Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)

from leancheck import check

def prop_not_idempotent(p:bool) -> bool:
    return (not (not p)) == p

def prop_and_commutes(p:bool, q:bool) -> bool:
    return (p and q) == (q and p)

def prop_or_commutes(p:bool, q:bool) -> bool:
    return (p or q) == (q or p)

# The following property is intentionally incorrect
def prop_and_or_interchangeable(p:bool, q:bool) -> bool:
    return (p and q) == (p or q)


check(prop_not_idempotent)
check(prop_and_commutes)
check(prop_or_commutes)
check(prop_and_or_interchangeable)
