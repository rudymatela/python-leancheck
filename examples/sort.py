#!/bin/bash
#
# Example: using LeanCHeck to test sorting functions
#
# (C) 2023-2024  Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)
#
#
# In this example, we test properties for the functional/pure and the
# effectful/impure interfaces for sorting in Python.  LeanCheck works for both.

import leancheck

# Properties about the functional "sorted()" interface

# Sorting once is the same as sorting twice
def prop_sorted_twice(xs: list[int]) -> bool:
    return sorted(sorted(xs)) == sorted(xs)

# After sorting, the list should not change its length
def prop_sorted_len(xs: list[int]) -> bool:
    return len(sorted(xs)) == len(xs)

# This is an incorrect property about sort.
# LeanCheck should provide a counterexample.
def prop_sorted_wrong(xs: list[int]) -> bool:
    return sorted(xs) == xs


# Properties about the imperative ".sort()" interface

# Sorting once is the same as sorting twice.
def prop_sort_twice(xs: list[int]) -> bool:
    xs.sort()
    ys = list(xs)
    xs.sort()
    return xs == ys

# After sorting, the list should retain all elements in the original list.
def prop_sort_elem(x: int, xs: list[int]) -> bool:
    ys = list(xs)
    ys.sort
    return (x in ys) == (x in xs)

# This is an incorrect property about sort.
# LeanCheck should provide a counterexample.
def prop_sort_wrong(xs: list[int]) -> bool:
    ys = list(xs)
    xs.sort()
    return xs == ys

# We could check the properties explicitly like so:
# check(prop_sorted_twice)
# check(prop_sorted_len)
# check(prop_sorted_wrong)
# check(prop_sort_twice)
# check(prop_sort_elem)
# check(prop_sort_wrong)

# ... but we instead call leancheck.main()
# which tests all functions starting with prop_
leancheck.main(exit_on_failure=False)
